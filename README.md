# beaver fastapi server

- just run below cmd

```bash
git clone https://github.com/inha-carbon-neutral-seven/beaver-web-server.git
./make.sh 
```

## todo

- [ ] https // https://nginxproxymanager.com/
- [x] 린트 적용 ( ci cd ), precommit -> pre-commit-config.yaml 만들기
- [x] cicd 구축
- [x] 학교에 서버 설치 후 ddns 연결
- [ ] 테스트 코드 작성

## how to use pre-commit

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