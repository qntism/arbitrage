// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6;

interface bzxRead{
  function getLoan ( bytes32 loanId ) external view returns ( bytes32 loanId1, uint96 endTimestamp, address loanToken, address collateralToken, uint256 principal, uint256 collateral, uint256 interestOwedPerDay, uint256 interestDepositRemaining, uint256 startRate, uint256 startMargin, uint256 maintenanceMargin, uint256 currentMargin, uint256 maxLoanTerm, uint256 maxLiquidatable, uint256 maxSeizable);
}

interface bzxWrite{
  function liquidate(bytes32 loanId, address receiver, uint256 closeAmount) external;
}

interface UniswapV2{
   function addLiquidity ( address tokenA, address tokenB, uint256 amountADesired, uint256 amountBDesired, uint256 amountAMin, uint256 amountBMin, address to, uint256 deadline ) external returns ( uint256 amountA, uint256 amountB, uint256 liquidity );
   function addLiquidityETH ( address token, uint256 amountTokenDesired, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline ) external returns ( uint256 amountToken, uint256 amountETH, uint256 liquidity );
   function removeLiquidityETH ( address token, uint256 liquidity, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline ) external returns ( uint256 amountToken, uint256 amountETH );
   function removeLiquidity ( address tokenA, address tokenB, uint256 liquidity, uint256 amountAMin, uint256 amountBMin, address to, uint256 deadline ) external returns ( uint256 amountA, uint256 amountB );
   function swapExactETHForTokens ( uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[]  memory amounts );
   function swapExactTokensForTokens ( uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline ) external returns ( uint256[] memory amounts );
   function getAmountsOut(uint amountIn, address[] calldata path) external view returns (uint[] memory amounts);
}

interface FlashLoanInterface {
      function flashLoan(address _receiver, address _reserve, uint256 _amount, bytes calldata  _params) external;
}

interface ERC20 {
    function totalSupply() external view returns(uint supply);
    function balanceOf(address _owner) external view returns(uint balance);
    function transfer(address _to, uint _value) external returns(bool success);
    function transferFrom(address _from, address _to, uint _value) external returns(bool success);
    function approve(address _spender, uint _value) external returns(bool success);
    function allowance(address _owner, address _spender) external view returns(uint remaining);
    function decimals() external view returns(uint digits);
    event Approval(address indexed _owner, address indexed _spender, uint _value);
}

contract bzxliquidate{
  address payable owner;
   address ETH_TOKEN_ADDRESS  = address(0x0);
   address aaveRepaymentAddress = 0x3dfd23A6c5E8BbcFc9581d2E864a68feb6a076d3;

   bzxRead bzx0= bzxRead(0x103936aEC861d7CFb2d5c7F9dd1a671085f5fDd3);
   bzxWrite bzx1 = bzxWrite(0xD8Ee69652E4e4838f2531732a46d1f7F584F0b7f);
   UniswapV2 usi = UniswapV2(0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D);
   FlashLoanInterface fli = FlashLoanInterface(0x398eC7346DcD622eDc5ae82352F02bE94C62d119);
   bytes theBytes;

   address currentCToken;
   address currentLToken ;
   uint256  currentMaxLiq;
   bytes32 currentLoanId;

   modifier onlyOwner() {
       if (msg.sender == owner) _;
     }

constructor() public payable {
  owner = msg.sender;
}

function kickAss(bytes32 loanId, address receiver, uint256 closeAmount) onlyOwner public{
    //getLoan
    //get amount  and which token you need to pay / flash loan borrow
    (bytes32 loanId1, uint96 endTimestamp, address loanToken, address collateralToken, uint256 principal, uint256 collateral, , , , , , uint256 currentMargin, uint256 maxLoanTerm, uint256 maxLiquidatable, uint256 maxSeizable) = bzx0.getLoan(loanId);
   currentCToken = collateralToken;
   currentLToken = loanToken;
   currentMaxLiq = maxLiquidatable;
   currentLoanId = loanId;

    fli.flashLoan(address(this), loanToken, maxLiquidatable, theBytes);

    //flash borrow that amount

    //and then flash function will call bzx liquidate function, swap the returned token from to our repayment  tokenof aave, and pay back avave with fee
}

     function performUniswap(address sellToken, address buyToken, uint amount) public returns (uint256 amounts1){
             address [] memory addresses = new address[](2);
             addresses[0] = sellToken;
             addresses[1] = buyToken;

             uint256 [] memory amounts = performUniswapActual(addresses, amount );
             uint256 resultingTokens = amounts[1];
             return resultingTokens;
      }

      function performUniswapActual(address  [] memory theAddresses, uint amount) public returns (uint256[] memory amounts1){
             //uint256  amounts = uniswapContract.getAmountsOut(amount,theAddresses );
             uint256 deadline = 1000000000000000;
             uint256 [] memory amounts =  usi.swapExactTokensForTokens(amount, 1, theAddresses, address(this),deadline );
             return amounts;
      }

  function performTrade() public onlyOwner{

      ERC20 bzLToken = ERC20(currentLToken);

      if(bzLToken.allowance(address(this), bzx1Address)<=currentMaxLiq){
             bzLToken.approve(bzx1Address,  1000000000000000000000000000000000);
      }

      bzx1.liquidate(currentLoanId, address(this), currentMaxLiq);
      ERC20 tokenToReceive = ERC20(currentLToken);
      performUniswap(currentCToken, currentLToken, tokenToReceive.balanceOf(address(this)));
  }

  function executeOperation(address _reserve, uint256 _amount, uint256 _fee, bytes calldata  _params) external {
        performTrade();
        ERC20 firstToken = ERC20(_reserve);
        firstToken.transfer(aaveRepaymentAddress, (_amount+_fee));
    }


  function changeOwner(address payable newOwner) public  onlyOwner{
      owner = newOwner;
  }

  function getTokenBalance(address tokenAddress) public view returns(uint256){
    ERC20 theToken = ERC20(tokenAddress);
    return theToken.balanceOf(address(this));
  }

  function withdraw(address token, uint amount, address payable destination) public onlyOwner returns(bool) {
        if (address(token) == ETH_TOKEN_ADDRESS) {
            destination.transfer(amount);
        }
        else {
            ERC20 tokenToken = ERC20(token);
            require(tokenToken.transfer(destination, amount));
        }
        return true;
    }


    function kill() virtual public {
            if (msg.sender == owner){
                selfdestruct(owner);
            }
   }
}
