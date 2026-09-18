-- 1. 특정 컬럼 조회
SELECT * FROM employees;
SELECT emp_no, first_name, family_name, mobile FROM employees;

-- 산술 표현 (계산 결과 보여주기)
-- as는 긴 컬럼명을 단축명으로 만들어준다. (alias)
SELECT first_name, family_name, salary/10000 as 급여 FROM employees;

-- 문자열 합치기
SELECT 
	CONCAT(family_name, first_name) as 이름
	, CONCAT(salary/10000, '만원') as 급여
FROM employees;

-- 숫자 + 문자를 하면 숫자가 소수점으로 표현된다.
-- 이럴경우 TRUNCATE(숫자, 남길소수점)을 통해 정리해주면 된다.
SELECT 
	CONCAT(family_name, first_name) as 이름
	, CONCAT(TRUNCATE(salary/10000,0), '만원') as 급여
FROM employees;

-- 2. 조건 (WHERE)
SELECT * FROM employees e WHERE e.family_name = '김';
SELECT * FROM employees e WHERE e.salary > 3000000;
-- AND
SELECT e.family_name, e.first_name, e.salary
	FROM employees e WHERE e.salary >=1000000 AND e.salary <= 5000000;

-- BEWTWEEN AND
-- 숫자에만 적용 (잘 사용되지 않는다.) / <>와 같은 부등호가 태그로 인식될 경우 사용
SELECT e.family_name, e.first_name, e.salary
	FROM employees e WHERE e.salary BETWEEN 1000000 AND 5000000;

-- OR
SELECT * FROM employees e WHERE e.family_name = '김' OR e.salary = 2000000;

-- 중복 제거
-- SELECT DISTINCT [출력할 컬럼] FROM [테이블]
-- DISTINCT 이후의 컬럼에 대해서 중복을 제거 후 출력
SELECT e.family_name FROM employees e ORDER BY e.family_name ASC;
SELECT DISTINCT e.family_name FROM employees e ORDER BY e.family_name ASC;

SELECT e.family_name, e.salary FROM employees e ORDER BY e.family_name;

-- e.family_name과 e.salary를 조합한 내용이 중복된 경우만 제거
SELECT DISTINCT e.family_name, e.salary FROM employees e ORDER BY e.family_name;

-- IN 절 (여러 OR 조건을 하나로 합친..)
SELECT * FROM employees e WHERE e.family_name = '김' OR e.family_name = '이' OR e.family_name = '박';
-- 장점 : 간결하다. 속도가 빠르다.
-- 한계점 : 모든 OR가 동일한 컬럼을 대상으로 해야한다.
SELECT * FROM employees e WHERE e.family_name IN ('김', '이', '박');

-- LIKE
-- 일부가 비슷한 내용을 검색
-- WHERE [컬럼명] LIKE '%문자열%'
-- ze%    : ze 이후로 아무거나 와도 된다. -> ze로 시작하는 문장
-- %com   : com으로 끝나는 문장
-- %se%   : se를 포함하는 문장
-- %s%e%  : s와 e를 포함하는 문장
SELECT e.email FROM employees e WHERE e.email LIKE 'ze%';
SELECT e.email FROM employees e WHERE e.email LIKE '%com';
SELECT e.email FROM employees e WHERE e.email LIKE '%se%';
SELECT e.email FROM employees e WHERE e.email LIKE '%s%e%';

-- 3. 정렬 (ORDER BY)
-- ORDER BY [컬럼명] [ASC | DESC]
-- 조건 검색 > 정렬
SELECT * FROM employees e WHERE e.salary > 2000000 ORDER BY e.salary DESC;

-- salary로 내림차순, 동률에 대해서 first_name 오름차순
SELECT * FROM employees e WHERE e.salary > 2000000 ORDER BY e.salary DESC, e.family_name ASC;

-- GROUP BY
-- 데이터의 특정 컬럼을 기준으로 묶어서 가져온다. (통계)
SELECT * FROM employees e;
SELECT DISTINCT e.depart_no FROM employees e ORDER BY e.depart_no;

-- dev001 ~ dev005 급여 총합
SELECT e.depart_no, e.salary FROM employees e;
SELECT e.depart_no, SUM(e.salary) FROM employees e WHERE e.depart_no = "dev001";
SELECT e.depart_no, SUM(e.salary) FROM employees e WHERE e.depart_no = "dev002";
SELECT e.depart_no, SUM(e.salary) FROM employees e WHERE e.depart_no = "dev003";
SELECT e.depart_no, SUM(e.salary) FROM employees e WHERE e.depart_no = "dev004";
SELECT e.depart_no, SUM(e.salary) FROM employees e WHERE e.depart_no = "dev005";

-- GROUP BY : 특정 기준으로 묶어서 보여줌 (각 기준별 1ROW가 나와야 하기 때문에 연산이 꼭 들어가야 함)
-- 연산이 들어가지 않으면 row의 가장 첫 값을 보여준다 (원래는 에러가 나타남)
SELECT e.depart_no, SUM(e.salary) as 총급여 FROM employees e GROUP BY e.depart_no;

-- 각 부서별 급여 합계 (SUM)와 인센티브(Commision)의 평균 (AVG)을 구해보자.
SELECT e.depart_no, 
	SUM(e.salary) as 총급여, 
	AVG(e.commission) as 성과급
FROM employees e GROUP BY e.depart_no;

-- 급여평균, 인원수
-- HAVING : GROUP BY 로 받아온 데이터에 대해서 조건을 주는 것 (WHERE)
SELECT
	e.depart_no,
	FLOOR(AVG(e.salary)) as 급여평균,
	COUNT(e.depart_no) as 인원
FROM employees e GROUP BY e.depart_no;

-- HAVING에 별칭이 통하지 않는 DB도 있다.
-- 그 경우 별칭을 주기 전 이름으로 사용해야 한다.
SELECT
	e.depart_no,
	FLOOR(AVG(e.salary)) as 급여평균,
	COUNT(e.depart_no) as 인원
FROM employees e GROUP BY e.depart_no HAVING FLOOR(AVG(e.salary)) > 5000000;






