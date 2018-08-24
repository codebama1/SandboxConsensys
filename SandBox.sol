pragma solidity ^0.4.24;
contract SandBox {
    // Our 'dict' of addresses that are approved to share codes
    mapping (address => bool) approvedDeveloper;
    string code;

    // Our event to post code on the blockchain
    event GitPushCode(address _developer, string code);
    // Our event to capture deployment of this contract
    event ContractDeployed(string _deployed);

    constructor() public {
        emit ContractDeployed("Contract Deployed");
    }

    // Because this function is 'payable' it will be called when ether is sent to the contract address.
    function() public payable{
        // msg is a special variable that contains information about the transaction
        if (msg.value > 10000000000000000) {
            //if the value sent greater than 0.01 ether (in Wei)
            // then add the sender's address to approvedSandboxer
            approvedDeveloper[msg.sender] =  true;
        }
    }
    // Our read-only function that checks whether the specified address is approved to post codes.
    function isApproved(address _developer) public view returns (bool approved) {
        return approvedDeveloper[_developer];
    }

    // Read-only function that returns the current code
    function getCurrentCode() public view returns(string) {
        return code;
    }
    //Our function that modifies the state on the blockchain
    function pushCode(string _code) public returns (bool success) {
        // Looking up the address of the sender will return false if the sender isn't approved
        if (approvedDeveloper[msg.sender]) {
            code = _code;
            emit GitPushCode(msg.sender, code);
            return true;

        } else {
            return false;
        }
    }
}
