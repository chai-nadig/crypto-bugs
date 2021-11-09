import {ALCHEMY_ADDRESS, ADDRESS, ABI} from "../../config.js"
import Web3 from "web3";

// import the json containing all metadata. not recommended, try to fetch the database from a middleware if possible, I use MONGODB for example
import traits from "../../database/traitsfinal.json";

const infuraAddress = ALCHEMY_ADDRESS

const bugsApi = async(req, res) => {

    // SOME WEB3 STUFF TO CONNECT TO SMART CONTRACT
  const provider = new Web3.providers.HttpProvider(infuraAddress)
  const web3infura = new Web3(provider);
  const bugsContract = new web3infura.eth.Contract(ABI, ADDRESS)

  // IF YOU ARE USING INSTA REVEAL MODEL, USE THIS TO GET HOW MANY NFTS ARE MINTED
   const totalSupply = await bugsContract.methods.totalSupply().call();
   console.log(totalSupply)
  

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
    // const trait = traits[ Math.floor(Math.random() * 8888) ] // for testing on rinkeby 

    // CHECK OPENSEA METADATA STANDARD DOCUMENTATION https://docs.opensea.io/docs/metadata-standards
    let metadata = {}
    // GENERAL BUG METADATA
    metadata = {
      "name": tokenName,
      "description": "",
      "tokenId" : parseInt(query),
      "image": `https://ipfs.io/ipfs/${trait["imageIPFS"]}`,
      "external_url":"https://crypto-bugs.com",
      "attributes": [
          {
            "trait_type": "Background",
            "value": trait["Background"]
          },
          {
            "trait_type": "Color",
            "value": trait["Color"]
          },
          {
            "trait_type": "Spots",
            "value": trait["Spots"]
          },
          {
            "trait_type": "Eyes",
            "value": trait["Eyes"]
          },
          {
            "trait_type": "Accessory",
            "value": trait["Accessory"]
          },
      ]
    }
      // console.log(metadata)
    res.statusCode = 200
    res.json(metadata)
  } else {
    console.log("We're here")
    res.statuscode = 404
    res.json({error: "The bug you requested is out of range"})
  }

  // this is after the reveal

}

export default bugsApi