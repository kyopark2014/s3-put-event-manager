# S3의 Put Object Event를 처리하기 위한 Event Manager

전체적인 Architecture는 아래와 같습니다.

![image](https://github.com/kyopark2014/event-manager/assets/52392004/abc14daa-4d3f-4d64-a1df-81eb178e7fef)


[Event Manager를 안쓰는 경우]

이때의 데이터 Flow는 아래와 같습니다.

```text
(1) - (2a-1) - (2a-2) - (3) - (4)
```

(1) Amazon S3로 다량의 Object들이 인입됩니다. 여기서는 Cloud9을 이용하여 터미널에서 작은 사이즈의 파일들을 업로드 합니다.
(2a-1) S3로 Object가 인입될때 발생하는 put event를 AWS Lambda가 받습니다.
(2a-2) Lambda는 SQS에 json 형태로 event를 저장합니다. 
(3) SQS에 event가 들어오면 Lambda (invoke)를 trigger합니다.
(4) Lambda (invoke)가 Step Fucntions으로 event를 전달합니다. 

[Event Manager를 사용하는 경우]

Event Manager를 사용하는 경우에 아래와 같이 event를 처리하는 path가 변경됩니다.

```text
(1) - (2b-1) - (2b-2) - (2b-3) - (2b-4) - (3) - (4)
```

이때의 상세한 동작은 아래와 같습니다. 

(1) Amazon S3로 다량의 Object들이 인입됩니다. 여기서는 Cloud9을 이용하여 터미널에서 작은 사이즈의 파일들을 업로드 합니다.
(2b-1) S3로 Object가 인입될때 발생하는 put event를 AWS Lambda(S3-event)가 받습니다.
(2b-2) Lambda(S3-event)는 DyanmoDB json 형태로 event를 저장합니다. 
(2b-3) Event Bridge는 특정시간에 전체 event를 Trigger하기 위해 Lambda (event manager)를 Trigger 합니다.
(2b-4) Lambda (event manager)는 DynamoDB에서 event를 가져와서 SQS에 push 합니다.
(3) SQS에 event가 들어오면 Lambda (invoke)를 trigger합니다.
(4) Lambda (invoke)가 Step Fucntions으로 event를 전달합니다. 

