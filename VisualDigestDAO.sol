pragma solidity ^0.8.0;

contract VisualDigestDAO {
    address public owner;
    mapping(address => bool) public members;
    mapping(uint256 => mapping(address => bool)) public votes;
    mapping(uint256 => bool) public approvedOutputs;
    
    constructor() {
        owner = msg.sender;
        members[msg.sender] = true;
    }
    
    modifier onlyMember() {
        require(members[msg.sender], "Not a member");
        _;
    }
    
    function addMember(address _member) public {
        require(msg.sender == owner, "Only owner can add members");
        members[_member] = true;
    }
    
    function voteOnOutput(uint256 outputId, bool approve) public onlyMember {
        votes[outputId][msg.sender] = approve;
    }
    
    function isOutputApproved(uint256 outputId) public view returns (bool) {
        uint256 approvalCount = 0;
        for (uint256 i = 0; i < 100; i++) { // Limited loop for gas
            if (members[address(uint160(i))] && votes[outputId][address(uint160(i))]) {
                approvalCount++;
            }
        }
        return approvalCount > 1; // Simple majority (adjust as needed)
    }
}