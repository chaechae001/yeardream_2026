// test()       : 특정한 테스트 단위 의미
// expect()    : 테스트 실행 의미
// describe()  : test()의 group, describe는 describe를 담을 수 있다.

// describe('묶음에 대한 설명', 함수)
import {divide, minus, multiply, plus} from "@/app/calcModule";

describe('사칙연산 통합 테스트(정상, 에러)', function(){

    describe('사칙연산 테스트', function(){
        test('더하기 모듈 테스트', function(){
            expect(plus(10,30)).toBe(40);
        });
        test('빼기 모듈 테스트', function(){
            expect(minus(40,30)).toBe(10);
        });
        test('곱하기 모듈 테스트', function(){
            expect(multiply(10,30)).toBe(300);
        });
        test('나누기 모듈 테스트', function(){
            expect(divide(4,2)).toBe(2);
        });
    });

    describe('사칙연산 에러 테스트', function(){
        test('a 보다 b 값이 클 경우', function (){
            // throws 사용 시 실행함수를 한번 더 감싸준다.
            expect(()=> minus(10, 30)).toThrow('뺄셈의 값은 0보다 커야 합니다.');
        });

        test('0으로 나누기 시도', function(){
            expect(()=> divide(4,0)).toThrow('0으로 나눌 수 없습니다.');
        });
    });
});


/*
toBe() : 숫자, 문자, 불리언 타입의 값에 일치
toEqual()  : 객체나 배열의 일치
toContain() : 배열이나 문자열 내에 특정 값 포함 여부
toMatch() : 문자열이 지정된 정규표현식 패턴에 일치하는 지
toThrow() : 특정 에러가 발생하는 지 여부
 */
