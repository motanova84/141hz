import hre from "hardhat";

async function main() {
  console.log("🚀 Desplegando CoinQCAL...\n");

  const [deployer] = await hre.ethers.getSigners();
  console.log(`📍 Deployer: ${deployer.address}`);
  console.log(`💰 Balance: ${hre.ethers.formatEther(await hre.ethers.provider.getBalance(deployer.address))} ETH\n`);

  const CoinQCAL = await hre.ethers.getContractFactory("CoinQCAL");
  const coin = await CoinQCAL.deploy();
  await coin.waitForDeployment();

  const addr = await coin.getAddress();
  console.log(`✅ CoinQCAL desplegado en: ${addr}`);
  console.log(`🔗 Chain ID: ${(await hre.ethers.provider.getNetwork()).chainId}`);
  console.log(`\n📊 Parámetros:`);
  console.log(`   Génesis: ${hre.ethers.formatEther(await coin.GENESIS_SUPPLY())} QCAL`);
  console.log(`   Minado diario/nodo: ${hre.ethers.formatEther(await coin.DAILY_RATE())} QCAL`);
  console.log(`   Nodos: ${await coin.nodeCount()}`);
  console.log(`   Total minado: ${hre.ethers.formatEther(await coin.totalMined())} QCAL`);
  console.log(`   Owner/Nodo 1: ${await coin.owner()}`);
  console.log(`\n∴𓂀Ω∞³Φ · f₀ = 141.7001 Hz`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
