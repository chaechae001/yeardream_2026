// test()       : 특정한 테스트 단위 의미
// expect()    : 테스트 실행 의미
// describe()  : test()의 group, describe는 describe를 담을 수 있다.

// describe('묶음에 대한 설명', 함수)
import {render, screen} from "@testing-library/react";
import App from "@/app/page";
import {userEvent} from "@testing-library/user-event/dist/cjs/setup/index.js";

async function calcTestUI(val1, val2, operVal, answer){
        // 1. UI 가져옴
        // 테스트할 UI는 App에 있으므로 App에서 UI 가져옴
        const {container} = render(<App/>);
        // 2. 원하는 요소 확보
        const su1 = container.querySelector('input[name="su1"]');
        const su2 = container.querySelector('input[name="su2"]');
        const oper = container.querySelector('select[name="oper"]');
        const btn = container.querySelector('button');
        const result = screen.getByTestId('result');
        // 3. 특정 이벤트 발생 시
        await userEvent.type(su1,val1);
        await userEvent.type(su2,val2);
        await userEvent.selectOptions(oper,operVal);
        await userEvent.click(btn);
        // 4. 특정한 결과 확인
        expect(result).toHaveTextContent(answer);
}

describe('사칙연산 UI 테스트', function(){
    test('더하기 테스트', async function(){
        await calcTestUI('10', '20', '+', '답 : 30');
    });
});

/*
toBe() : 숫자, 문자, 불리언 타입의 값에 일치
toEqual()  : 객체나 배열의 일치
toContain() : 배열이나 문자열 내에 특정 값 포함 여부
toMatch() : 문자열이 지정된 정규표현식 패턴에 일치하는 지
toThrow() : 특정 에러가 발생하는 지 여부
 */
