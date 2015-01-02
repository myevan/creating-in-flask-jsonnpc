Creating in FlaskJSONPRC
========================

개선 사항
-------

#### 요청

* 요청 데이터 "id"가 없으면 비어있는 응답 리턴
* 요청 데이터 "jsonrpc"가 없으면 응답 "error" 에 null 리턴
* 요청 데이터 "params" 타입이 안 맞아도 묵시적으로 타입 변환됨
