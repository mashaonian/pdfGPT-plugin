## Running on localhost

* create conda env

```bash
cd backend   # cd root file
conda create -n myenv python=3.9
conda activate myenv
```

* installing the dependencies

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple   
```

* start to deploy web application on port 3333

```bash
python plugins.py
```

## Reference

### Q1: how to download the Universal Sentence Encoder?

A: click to  [pdf repo](https://github.com/bhaskatripathi/pdfGPT?tab=readme-ov-file#running-on-localhost) to figure out how to solve this problem

### Q2: Is this a RAG application? how to learn the procedure of RAG application?

A:

1. refer to   [RAG procedure](https://mp.weixin.qq.com/s/hx84sb7c0GF5Xw2-mU7apQ) to understand how it works
2. refer to [RAG demo](https://mp.weixin.qq.com/s/RONG0mK07ZHrQZ5mgr31cg) to understand how to code
3. refer to [RAG improvements](https://mp.weixin.qq.com/s/LHCfxk5Z2h3g5jTda-c8TA) to know how to improve a RAG application
