-- 트랜잭션 : 쪼갤 수 없는 논리적 업무 단위
-- 실제로는 여러 단계이지만 한단계로 가정하는 것
-- 송금은 출금과 입금 2단계 이지만, 둘 중 하나라도 실패하면 송금은 취소된다.
-- 이때 작업을 확정하는 것을 commit
-- 작업을 취소하는 것을 rollback
-- SQL에서는 무조건 commit을 해야 작업이 확정된다.

-- 1) AUTOCOMMIT이 설정되어 있어서이다.
SELECT @@AUTOCOMMIT;  -- 1: 설정 / 2: 미설정

-- 2) AUTOCOMMIT 변경
SET @@AUTOCOMMIT = 0;
