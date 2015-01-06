Creating in FlaskJSONPRC
========================

개선 필요
---------

* 요청 데이터 "params" 타입이 안 맞아도 묵시적으로 타입 변환됨
* 인증 백엔드를 변경해도 username, password 처리 -> myevan 포크로 수정
* 멀티 버전 제대로 처리 안 됨 (하위 버전 메소드가 사라짐)


확인 내용
---------

* 요청 데이터 "jsonrpc"가 없으면 응답 "error" 에 null 리턴
    * JSON-RPC 1.0 스펙 처리
* 요청 데이터 "id"가 없으면 비어있는 응답 리턴
    * JSON RPC 스펙 Notification 요청
    * 204 No Content 리턴


참고 자료
---------

* JSON-RPC 스펙 <http://www.jsonrpc.org/specification>
