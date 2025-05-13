const fs = require('fs')
const path = require('path')

// 1. package.json에서 version 읽기
const pkgPath = path.join(__dirname, 'package.json')
const gradlePath = path.join(__dirname, 'android/app/build.gradle')
const versionJsonPath = path.join(__dirname, 'android/app/build/outputs/apk/debug/version.json')

const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'))
const version = pkg.version // 예: '1.2.3'

// 2. versionCode 계산 (1.2.3 → 1002003)
const versionCode = version.split('.')
  .map(v => v.padStart(2, '0'))
  .reduce((acc, v) => acc + v, '')
  .padEnd(7, '0') // 최소 3자리(1.0.0) 보장
const versionCodeInt = parseInt(versionCode, 10)

// 3. build.gradle 수정
let gradle = fs.readFileSync(gradlePath, 'utf8')
gradle = gradle.replace(/versionCode \d+/, `versionCode ${versionCodeInt}`)
gradle = gradle.replace(/versionName ".*"/, `versionName "${version}"`)
fs.writeFileSync(gradlePath, gradle)

// 4. version.json 자동 생성/갱신
const apkUrl = "http://223.130.139.218:8080/app-debug.apk" // 실제 배포 주소로 맞춰주세요
const versionJson = {
  latest: version,
  apkUrl
}
fs.writeFileSync(versionJsonPath, JSON.stringify(versionJson, null, 2))

console.log(`build.gradle, version.json 버전 갱신 완료: versionName=${version}, versionCode=${versionCodeInt}`) 