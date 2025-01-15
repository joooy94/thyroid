# thyroid

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5 llamafactory-cli train /root/thyroid/thyroid/src/model_config/llama3.2/post_training/llama3.2_lora_sft.yaml
```

```bash
CUDA_VISIBLE_DEVICES=6 llamafactory-cli export /root/thyroid/thyroid/src/model_config/llama3.2/inference/llama3.2_merge_lora_sft.yaml
```