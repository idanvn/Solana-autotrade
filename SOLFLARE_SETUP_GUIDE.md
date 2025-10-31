# Solflare Wallet Integration Guide

## 🔐 How to export your Solflare private key safely:

### Step 1: Open Solflare Wallet
1. Open your Solflare wallet (browser extension or app)
2. Make sure you're on the wallet you want to use for TESTING

### Step 2: Export Private Key
1. Click Settings (⚙️ gear icon)
2. Click "Export Private Key"  
3. Select "Array Format" or "JSON Array"
4. Copy the result (should look like: [1,2,3,4,...,64])

### Step 3: Set up .env file
Copy the array and paste it in your .env file like this:

```
# Your Solana RPC endpoint (get from Helius, QuickNode, etc.)
RPC_URL=https://your-mainnet-rpc-endpoint.com

# Your Solflare private key as JSON array (64 numbers)
WALLET_PRIVATE_KEY_JSON=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64]

# Jupiter/Orca API endpoints
JUPITER_BASE_URL=https://quote-api.jup.ag
```

## ⚠️ SAFETY WARNINGS:

1. **USE A TEST WALLET ONLY**
   - Never use your main wallet for bot testing
   - Create a separate wallet with small amounts ($10-20)

2. **NEVER SHARE YOUR PRIVATE KEY**
   - Don't commit .env to git
   - Don't paste it in chat/forum
   - Don't screenshot it

3. **START SMALL**
   - Test with <$5 trades first
   - Verify everything works before increasing amounts

4. **BACKUP YOUR SEED PHRASE**
   - Make sure you have your recovery words saved safely
   - Test recovery before using for trading

## 📱 Alternative: Hardware Wallet (Advanced)
For production use, consider using a hardware wallet (Ledger) 
with the bot for maximum security.

## 🚀 RPC Providers (choose one):

Free tier options:
- Helius: https://dev.helius.xyz
- QuickNode: https://quicknode.com  
- Alchemy: https://alchemy.com

Example RPC URLs:
- Helius: https://mainnet.helius-rpc.com/?api-key=your-key
- QuickNode: https://your-endpoint.solana-mainnet.quiknode.pro/your-key/

## 🧪 Testing Steps:

1. Set up .env with your test wallet
2. Run: python .\scripts\test_real_wallet.py
3. Complete the safety checklist
4. Execute micro trade test
5. If successful, enable full trading

Remember: Always test with tiny amounts first! 🛡️