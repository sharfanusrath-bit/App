// TaskContract.sol
pragma solidity ^0.8.0;

contract TaskContract {
    struct Evidence {
        uint id;
        address uploader;
        string fileHash;
        uint timestamp;
    }

    mapping(uint => Evidence) public evidences;
    uint public evidenceCount;

    function storeEvidence(string memory fileHash) public {
        evidenceCount++;
        evidences[evidenceCount] = Evidence(evidenceCount, msg.sender, fileHash, block.timestamp);
    }

    function getEvidence(uint _id) public view returns (uint, address, string memory, uint) {
        Evidence memory e = evidences[_id];
        return (e.id, e.uploader, e.fileHash, e.timestamp);
    }
}
