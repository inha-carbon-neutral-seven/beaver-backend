<div align="center">
  <br>
<p align="center" width="100%">
    <img src="docs/images/logo.png" alt="beaver icon" style="width: 140px; height:140px; display: block; margin: auto; border-radius: 80%;">
</p>
  
  <h2>비버.ai - 백엔드</h2></hr>
  <p align="center">
    <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=FastAPI&logoColor=white" alt="FastAPI badge">
    <img src="https://img.shields.io/badge/LangChain-339933?style=flat-square&logo=GitHub&logoColor=white" alt="LangChain badge">
    <img src="https://img.shields.io/badge/LlamaIndex-618AFB?style=flat-square&logo=GitHub&logoColor=white" alt="Llamaindex badge">
    <img src="https://img.shields.io/badge/pandas-%23150458.svg?style=flat-square&logo=pandas&logoColor=white" alt="Pandas badge">
    <img src="https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=flat-square&logo=scikit-learn&logoColor=white" alt="Scikit-learn badge">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=Docker&logoColor=white"/>
</div>

## pre-requisite
1. install `docker desktop` or `docker`
    - https://www.docker.com/products/docker-desktop/  
2. run `docker`

## How to setup Back-End Server
> just run below command

1. install beaver-backend
```bash
git clone https://github.com/inha-carbon-neutral-seven/beaver-backend.git

cd beaver-backend
```
2-1. Linux OS
```
./make.sh
```
2-2. Windows OS
```
./make.bat
```


## 개발 기간

2023.09.26. ~ 2024.02.27. (6개월)

---
## Further Reading

* [프로젝트 소개 노션](https://kangmoonseo.notion.site/ai-878925e8f8084fff81b170a4afddccae?pvs=4)









<!--
## todo

- [ ] https // https://nginxproxymanager.com/
- [x] 린트 적용 ( ci cd ), precommit -> pre-commit-config.yaml 만들기
- [x] cicd 구축
- [x] 학교에 서버 설치 후 ddns 연결
- [x] 테스트 코드 작성
-->

## To contributor: how to use pre-commit

install pre-commit on your local env

```python
pip install pre-commit
pre-commit install
pre-commit run --all-files // check setting 
```

![image](https://github.com/inha-carbon-neutral-seven/beaver-web-server/assets/80192345/18b3f95b-0199-4c4d-9c2d-f01b0ebe4f8b)


## 랭체인 문서 기록
https://python.langchain.com/docs/integrations/document_loaders/unstructured_file
https://python.langchain.com/docs/integrations/vectorstores/chroma
https://python.langchain.com/docs/modules/data_connection/document_loaders/file_directory
https://python.langchain.com/docs/use_cases/question_answering/quickstart

#### With Memory and returning source documents 
https://python.langchain.com/docs/expression_language/cookbook/retrieval