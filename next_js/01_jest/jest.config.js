// next와 jest를 연동
const nextJest = require("next/jest");

// 여기에 있는 설정 파일들을 읽어라 (설정 파일들은 이 공간에 다 있어)
const createJestConfig = nextJest({dir:'./'});

const jestConfig = {
    testEnvironment:'jest-environment-jsdom',
    moduleNameMapper:{
        // 정규표현식 시작 : ^$
        // ^@/(.)$ : @로시작하고 /가 들어가면 뒤에 특정한 (.)패턴이 들어감
        // .은 임의의 글자
        // *은 연속되는 글자
        '^@/(.*)$':'<rootDir>/src/$1'
    }
};

module.exports = createJestConfig(jestConfig);