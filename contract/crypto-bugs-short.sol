pragma solidity ^0.7.0;
pragma abicoder v2;


import "@openzeppelin/contracts@3.3.0/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts@3.3.0/access/Ownable.sol";
import "@openzeppelin/contracts@3.3.0/math/SafeMath.sol";

contract CryptoBugs is ERC721, Ownable  {

    using SafeMath for uint256;

    // IPFS URL WILL BE ADDED WHEN ALL BUGS ARE SOLD OUT
    string public BUG_PROVENANCE = "";

    string public LICENSE_TEXT = "";

    // TEAM CAN'T EDIT THE LICENSE AFTER THIS GETS TRUE
    bool licenseLocked = false;

    // Unit in WEI. 0.025 ETH
    uint256 public bugPrice = 25000000000000000;

    bool public saleIsActive = false;

    // Reserve 100 Bugs for team - Giveaways/Prizes etc
    uint256 public bugReserve = 100;

    event licenseisLocked(string _licenseText);

    // Mapping between addresses and how much money they have withdrawn. This is
    // used to calculate the balance of each account. The public keyword allows
    // reading from the map but not writing to the map using the
    // amountsWithdrew(address) method of the contract. It's public mainly for
    // testing.
    mapping(address => uint256) public amountsWithdrew;

    // A set of parties to split the funds between. They are initialized in the
    // constructor.
    mapping(address => bool) public between;

    // The number of ways incoming funds will we split.
    uint256 public numberOfSplits;

    // The total amount of funds which has been deposited into the contract.
    uint256 public totalFunds;


    /// @param addrs The address received funds will be split between.
    constructor(address[] memory addrs) ERC721("crypto-bugs-0x2b67", "cb0x2b67") {
        // Contracts can be deployed to addresses with ETH already in them. We
        // want to call balance on address not the balance function defined
        // below so a cast is necessary.
        totalFunds = address(this).balance;

        numberOfSplits = addrs.length;

        for (uint256 i = 0; i < addrs.length; i++) {
            // loop over addrs and update set of included accounts
            between[addrs[i]] = true;
        }
    }

    function setProvenanceHash(string memory provenanceHash) public onlyOwner {
        BUG_PROVENANCE = provenanceHash;
    }

    // Change the license
    function changeLicense(string memory _license) public onlyOwner {
        require(licenseLocked == false, "License already locked");
        LICENSE_TEXT = _license;
    }

    // Locks the license to prevent further changes
    function lockLicense() public onlyOwner {
        licenseLocked =  true;
        emit licenseisLocked(LICENSE_TEXT);
    }

    /// @notice Sets the bug price.
    /// @param price The price in wei per bug.
    function setBugPrice(uint256 price) public onlyOwner {
        bugPrice = price;
    }

    function flipSaleState() public onlyOwner {
        saleIsActive = !saleIsActive;
    }

    function reserveBugs(address _to, uint256 _reserveAmount) public onlyOwner {
        require(_reserveAmount > 0 && _reserveAmount <= bugReserve, "Not enough bug reserve left for team");
        require(totalSupply().add(_reserveAmount) <= 11111, "Reserve amount would exceed max supply of bugs");

        uint256 supply = totalSupply();
        for (uint256 i = 0; i < _reserveAmount; i++) {
            _safeMint(_to, supply + i);
        }
        bugReserve = bugReserve.sub(_reserveAmount);
    }

    function setBaseURI(string memory baseURI) public onlyOwner {
        _setBaseURI(baseURI);
    }


    function tokensOfOwner(address owner) external view returns(uint256[] memory ) {
        uint256 tokenCount = balanceOf(owner);
        if (tokenCount == 0) {
            // Return an empty array
            return new uint256[](0);
        } else {
            uint256[] memory result = new uint256[](tokenCount);
            uint256 index;
            for (index = 0; index < tokenCount; index++) {
                result[index] = tokenOfOwnerByIndex(owner, index);
            }
            return result;
        }
    }

    // Returns the license for tokens
    function tokenLicense(uint256 _id) public view returns(string memory) {
        require(_id < totalSupply(), "CHOOSE A BUG WITHIN RANGE");
        return LICENSE_TEXT;
    }

    function mintBugs(uint256 numberOfTokens) public payable {
        require(saleIsActive, "Sale must be active to mint bug");
        require(numberOfTokens > 0 && numberOfTokens <= 20, "Can only mint upto 20 bugs at a time");
        require(totalSupply().add(numberOfTokens) <= 11111, "Purchase would exceed max supply of bugs");
        require(msg.value >= bugPrice.mul(numberOfTokens), "Ether value sent is not correct");

        for(uint256 i = 0; i < numberOfTokens; i++) {
            uint256 mintIndex = totalSupply();
            if (totalSupply() < 11111) {
                _safeMint(msg.sender, mintIndex);
            }
        }
        totalFunds += bugPrice.mul(numberOfTokens);
    }

    /// @notice Withdraws all funds available to the sender and deposits them
    /// into the sender's account.
    /// Checks whether the sender is allowed to withdraw
    function withdrawAll() public {
        // Require the withdrawer to be included in `between` at contract
        // creation time.
        require(between[msg.sender]);

        // Decide the amount to withdraw based on the `all` parameter.
        uint256 transferring = balance();

        // Updates the internal state, this is done before the transfer to
        // prevent re-entrancy bugs.
        amountsWithdrew[msg.sender] += transferring;

        // Transfer funds from the contract to the sender. The gas for this
        // transaction is paid for by msg.sender.
        msg.sender.transfer(transferring);
    }

    // We do integer division (floor(a / b)) when calculating each share, because
    // solidity doesn't have a decimal number type. This means there will be a
    // maximum remainder of count - 1 wei locked in the contract. We ignore this
    // because it is such a small amount of ethereum (1 Wei = 10^(-18) Ethereum).
    // The extra Wei can be extracted by depositing an amount to make
    // totalFunds evenly divisible between numberOfSplits parties.

    /// @notice Gets the amount of funds in Wei available to the sender.
    function balance() public view returns (uint256) {
        if (!between[msg.sender]) {
            // The sender of the message isn't part of the split. Ignore them.
            return 0;
        }

        // `share` is the amount of funds which are available to each of the
        // accounts specified in the constructor.
        uint256 share = totalFunds / numberOfSplits;
        uint256 withdrew = amountsWithdrew[msg.sender];
        uint256 available = share - withdrew;

        assert(available >= 0 && available <= share);

        return available;
    }
}