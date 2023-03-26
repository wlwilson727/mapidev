import requests
import json

# Specify the Codius host URL and smart contract code
codius_url = "https://mapi.global"
smart_contract_code = """
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract PatientNFT is ERC721 {
    uint256 public tokenCounter;

    constructor() ERC721("PatientNFT", "PTNT") {
        tokenCounter = 0;
    }

    struct Patient {
        string name;
        string dob;
        string[] encounterNotes;
    }

    mapping(uint256 => Patient) public patients;

    function createNFT(string memory name, string memory dob, string[] memory encounterNotes) public returns (uint256) {
        uint256 tokenId = tokenCounter;

        Patient memory newPatient = Patient(name, dob, encounterNotes);
        patients[tokenId] = newPatient;

        _safeMint(msg.sender, tokenId);
        tokenCounter++;

        return tokenId;
    }

    function getPatientName(uint256 tokenId) public view returns (string memory) {
        return patients[tokenId].name;
    }

    function getDob(uint256 tokenId) public view returns (string memory) {
        return patients[tokenId].dob;
    }

    function getEncounterNotes(uint256 tokenId) public view returns (string[] memory) {
        return patients[tokenId].encounterNotes;
    }
}
"""

# Compile the smart contract
response = requests.post(f"{codius_url}/compile", json={"language": "solidity", "code": smart_contract_code})
response_data = response.json()
compiled_code = response_data["result"]["bytecode"]

# Deploy the smart contract
response = requests.post(f"{codius_url}/deploy", json={"language": "solidity", "bytecode": compiled_code})
response_data = response.json()
smart_contract_address = response_data["result"]["address"]

# Mint a new NFT
patient_name = "John Doe"
dob = "01/01/1970"
encounter_notes = ["Note 1", "Note 2", "Note 3"]
response = requests.post(f"{codius_url}/invoke/{smart_contract_address}", json={
    "function": "createNFT",
    "args": [patient_name, dob, encounter_notes],
    "maxFee": "1000000"
})
response_data = response.json()
token_id = int(response_data["result"]["return"])

# Retrieve NFT metadata
response = requests.post(f"{codius_url}/invoke/{smart_contract_address}", json={
    "function": "getPatientName",
    "args": [token_id]
})
response_data = response.json()
patient_name = response_data["result"]["return"]

response = requests.post(f"{codius_url}/invoke/{smart_contract_address}", json={
    "function": "getDob",
    "args": [token_id]
})
response_data = response.json()
dob = response_data["result"]["return"]

response = requests.post(f"{codius_url}/invoke/{smart_contract_address}", json={
    "function": "getEncounterNotes",
    "args": [token_id]
})
response_data = response.json()
encounter_notes = response_data["result"]["return"]