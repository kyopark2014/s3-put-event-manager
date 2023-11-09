# S3의 Put Object Event를 처리하기 위한 Event Manager

여기서는 S3에 다수의 Obejct가 인입되어 다수의 Step functions이 수행될때에 Event를 관리하는 방법에 대해 설명합니다. AWS Step Functions의 처리 속도가 충분히 빠른 경우에는 Event Manager없이 SQS(FIFO)와 Lambda를 통하여 Event를 처리할 수 있습니다. 이때 DLQ를 같이 사용하면 실패 경우에도 자연스럽게 Event를 안정적으로 관리할 수 있습니다. 그런데 Step Functions의 처리 속도가 이벤트의 인입 속도에 비해 월등히 느리다면 안정적인 부하 관리를 위해 Event Manager를 이용할 수 있습니다. 아래 그림에서는 2가지 경우의 전체적인 Archtiectrue의 예를 보여주고 있습니다.

<img src="https://github.com/kyopark2014/s3-put-event-manager/assets/52392004/36622b19-f1c9-443f-ab93-6abb1d55b0ad" width="900">

## Event Manager를 사용하지 않는 경우

이때의 데이터 Flow는 아래와 같습니다.

```text
(1) - (2a-1) - (2a-2) - (3) - (4)
```

단계 1: Amazon S3로 다량의 Object들이 인입됩니다. 여기서는 Cloud9을 이용하여 터미널에서 작은 사이즈의 파일들을 업로드 합니다.

단계 2a-1: S3로 Object가 인입될때 발생하는 put event를 AWS Lambda가 받습니다.

단계 2a-2: Lambda는 SQS에 json 형태로 event를 저장합니다. 

단계 3: SQS에 event가 들어오면 Lambda (invoke)를 trigger합니다.

단계 4: Lambda (invoke)가 Step Fucntions으로 event를 전달합니다. 

## Event Manager를 사용하는 경우

Event Manager를 사용하는 경우에 아래와 같이 event를 처리하는 path가 변경됩니다.

```text
(1) - (2b-1) - (2b-2) - (2b-3) - (2b-4) - (3) - (4)
```

이때의 상세한 동작은 아래와 같습니다. 

단계 1: Amazon S3로 다량의 Object들이 인입됩니다. 여기서는 Cloud9을 이용하여 터미널에서 작은 사이즈의 파일들을 업로드 합니다.

단계 2b-1: S3로 Object가 인입될때 발생하는 put event를 AWS Lambda(S3-event)가 받습니다.

단계 2b-2: Lambda(S3-event)는 DyanmoDB json 형태로 event를 저장합니다. 

단계 2b-3: Event Bridge는 특정시간에 전체 event를 Trigger하기 위해 Lambda (event manager)를 Trigger 합니다.

단계 2b-4: Lambda (event manager)는 DynamoDB에서 event를 가져와서 SQS에 push 합니다.

단계 3: SQS에 event가 들어오면 Lambda (invoke)를 trigger합니다.

단계 4: Lambda (invoke)가 Step Fucntions으로 event를 전달합니다. 


상세한 Call Flow는 아래를 참조합니다.

![noname](https://github.com/kyopark2014/s3-put-event-manager/assets/52392004/1db24f03-8fd9-4c31-a619-41b41e32d4d0)

## 인프라 설치

[deployment.md](./deployment.md)에 인프라를 설치하고 필요한 셈플 파일을 다운로드 합니다.

## 실행 방법

