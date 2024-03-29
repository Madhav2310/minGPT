{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"pygments_lexer":"ipython3","nbconvert_exporter":"python","version":"3.6.4","file_extension":".py","codemirror_mode":{"name":"ipython","version":3},"name":"python","mimetype":"text/x-python"},"kaggle":{"accelerator":"none","dataSources":[],"isInternetEnabled":true,"language":"python","sourceType":"script","isGpuEnabled":false}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# %% [code]\n# # This Python 3 environment comes with many helpful analytics libraries installed\n# # It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python\n# # For example, here's several helpful packages to load\n\n# import numpy as np # linear algebra\n# import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)\n\n# # Input data files are available in the read-only \"../input/\" directory\n# # For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory\n\n# import os\n# for dirname, _, filenames in os.walk('/kaggle/input'):\n#     for filename in filenames:\n#         print(os.path.join(dirname, filename))\n\n# # You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using \"Save & Run All\" \n# # You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session\n\n# %% [code]\nimport torch\nimport torch.nn as nn\nfrom torch.nn import functional as F\n\n# %% [code]\n# Hyperparameters\nbatch_size = 32\nblock_size = 8\nmax_iters = 4000\neval_intervals = 300\nlearning_rate = 1e-2\ndevice = 'cuda' if torch.cuda.is_available\neval_iters = 200\n\n# %% [code]\nwith open('input.txt', 'r', encoding = 'utf-8') as f:\n    text = f.read()\n\n# %% [code]\nchars = sorted(list(set(text)))\nvocab_size = len(chars)\n#mappings\nstoi = [i:s for s,i in enumerate(chars)]\nitos = [i:s for i,s in enumerate(chars)]\nencode = lambda s: [stoi(c) for c in s]\ndecode = lambda l: [itos(c) for c in l]\n\n\n\n# %% [code]\n#splits\ndata = torch.tensor(encode(text), dtype = torch.long)\nn = int(0.9*len(data))\ntrain_data = data[:n]\nval_data = data[n:]\n\n# %% [code]\ndef get_batch(split):\n    data = train_data if slit == 'train' else val_data\n    ix = torch.randint(len(data) - block_size, (batch_size,))\n    x = torch.stack([data[i:i+block_size] for i in ix])\n    y = torch.stack([data[i+1:i+block_size+1] for i in ix])\n    x, y = x.to(device), y.to(device)\n    return x,y\n\n\n# %% [code]\n@torch.no_grad()\ndef estimate_loss():\n    out = {}\n    model.eval()\n    for split in ['train', 'test']:\n        losses = torch.zeroes(eval_iters)\n        for k in range(eval_iters):\n            X, Y = get_batch(split)\n            logits,loss = model(X, Y)\n            losses[k] = losses.mean()\n        out[split] = losses.mean()\n    model.train()\n    return out\n\n# %% [code]\nclass BigramLangModel(nn.Module):\n    \n    def __init__():\n        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)\n    \n    def forward(self,idx, targets = None):\n        logits = self.token_embedding_table(idx)__ # (B,T,C)\n        \n        if targets is None:\n            loss = None\n        else:\n            B, T, C = logits.shape\n            logits = togits.view(B*T, C)\n            targets = targets.view(B*T)\n            loss = F.cross_entropy(logits, targets)\n        return logits, loss\n    \n    def generate(self, idx, max_new_tokens):\n        for _ in range(max_new_tokens):\n            logits, loss  = self(idx)\n            logits = logits[:, -1, :]\n            probs = F.softmax(logits, dim = -1)\n            idx_next = torch.multinomial(probs, num_samples = 1)\n            idx = torch.cat((idx, idx_next), dim = 1)\n        return idx\n    model = BigramLangModel(vocab_size)\n    m = model.to(device)\n    \n    optimizer = torch.optim.AdamW(model.parameters(), lr = learning_rate)\n    \n    for iter in range(max_iters):\n        if iter%eval_interval ==0:\n            losses = estimate_loss()\n            print(f\"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}\")\n            \n        xb, yb = get_batch('train')\n        \n        logits, loss = model(xb, yb)\n        optimizer.zero_grad(set_to_none = True)\n        loss.backword()\n        optimizer.step()\n    context = torch.zeroes((1,1), dtype = torch.long, device = device)\n    print(decode(m.generate(context, max_new_tokens = 500)[0].tolist()))\n    ","metadata":{"_uuid":"1ff8ca4d-0877-4c3b-b01d-472931dd8f96","_cell_guid":"6e70c29e-9cd1-4a38-8285-69e9de18a387","collapsed":false,"jupyter":{"outputs_hidden":false},"trusted":true},"execution_count":null,"outputs":[]}]}