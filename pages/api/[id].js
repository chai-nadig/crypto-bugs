import {ALCHEMY_ADDRESS, ADDRESS, ABI} from "../../config.js"
import Web3 from "web3";

// import the json containing all metadata. not recommended, try to fetch the database from a middleware if possible, I use MONGODB for example
import traits from "../../database/traitsfinal.json";

const infuraAddress = ALCHEMY_ADDRESS

const bugsApi = async(req, res) => {

    // SOME WEB3 STUFF TO CONNECT TO SMART CONTRACT
  const provider = new Web3.providers.HttpProvider(infuraAddress)
  const web3alchemy = new Web3(provider);
  const bugsContract = new web3alchemy.eth.Contract(ABI, ADDRESS)

  // IF YOU ARE USING INSTA REVEAL MODEL, USE THIS TO GET HOW MANY NFTS ARE MINTED
   const totalSupply = await bugsContract.methods.totalSupply().call();


// THE ID YOU ASKED IN THE URL
  const query = req.query.id;

  // IF YOU ARE USING INSTA REVEAL MODEL, UNCOMMENT THIS AND COMMENT THE TWO LINES BELOW
   if(parseInt(query) < totalSupply) {
//  const totalBugs = 11111;
//  if(parseInt(query) < totalBugs) {
    // CALL CUSTOM TOKEN NAME IN THE CONTRACT
    const tokenNameCall = await bugsContract.methods.bugNames(query).call();
    let tokenName = `#${query}${(tokenNameCall === '') ? "" : ` - ${tokenNameCall}`}`

    // IF YOU ARE NOT USING CUSTOM NAMES, JUST USE THIS
    // let tokenName= `#${query}`

    const trait = traits[parseInt(query)]

    // CHECK OPENSEA METADATA STANDARD DOCUMENTATION https://docs.opensea.io/docs/metadata-standards
    let metadata = {}
    // GENERAL BUG METADATA

    let attributes = [];
    if (trait['Background']) {
      attributes.push({
        "trait_type": "Background",
        "value": trait["Background"]
      });
    }

    if (trait['Color']) {
      attributes.push({
        "trait_type": "Color",
        "value": trait["Color"]
      });
    }

    if (trait['Spots']) {
       attributes.push({
         "trait_type": "Spots",
         "value": trait["Spots"]
      });
    }

    if (trait['Eyes']) {
      attributes.push({
        "trait_type": "Eyes",
        "value": trait["Eyes"]
      });
    }

    if (trait['Accessory']) {
      attributes.push({
        "trait_type": "Accessory",
        "value": trait["Accessory"]
      });
    }

    if (trait['Severity']) {
      attributes.push({
        "trait_type": "Severity",
        "value": trait["Severity"]
      });
    }

    metadata = {
      "name": tokenName,
      "description": "",
      "tokenId" : parseInt(query),
      "image": `https://gateway.pinata.cloud/ipfs/${trait["imageIPFS"]}`,
      "external_url":"https://crypto-bugs.com",
      "attributes": attributes,
    }
      // console.log(metadata)
    res.statusCode = 200
    res.json(metadata)
  } else {
    res.statuscode = 404
    res.json({error: "The bug you requested is out of range"})
  }
}

export default bugsApi