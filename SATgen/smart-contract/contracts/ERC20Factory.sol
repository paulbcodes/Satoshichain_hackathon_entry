// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./TokenData.sol";
import "./CustomERC20.sol";

contract ERC20Factory {
    mapping(address => Token[]) private addressToTokens;

    event Created(string _name, string _symbol, string _tokenType, address _tokenAddress);

    function create(string memory name_, string memory symbol_, bool isBurnable_, bool isMintable_, uint256 initialSupply_) external returns (bool) {
        // Spin up new ERC20 token
        CustomERC20 erc20 = new CustomERC20(name_, symbol_, isBurnable_, isMintable_, initialSupply_);
        address _tokenAddress = address(erc20);

        // Save token data
        address sender = msg.sender;
        Token[] storage tokens = addressToTokens[sender];
        tokens.push(Token(name_, symbol_, "ERC20", isBurnable_, isMintable_, _tokenAddress));
        addressToTokens[sender] = tokens;

        // Emit and return
        emit Created(name_, symbol_, "ERC20", _tokenAddress);
        return true;
    }

    function getAll() public view returns(Token[] memory)
    {
        address sender = msg.sender;
        Token[] memory tokens = addressToTokens[sender];
        return tokens;
    }
}
