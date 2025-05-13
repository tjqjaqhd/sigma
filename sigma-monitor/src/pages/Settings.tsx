import React, { useEffect, useState, useRef } from 'react'
import {
  Box, Typography, Button, Card, CardContent, Divider, Fade, Snackbar, Alert, LinearProgress, Dialog, DialogTitle, DialogContent, DialogActions, IconButton
} from '@mui/material'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import WarningAmberRoundedIcon from '@mui/icons-material/WarningAmberRounded'
import SystemUpdateAltRoundedIcon from '@mui/icons-material/SystemUpdateAltRounded'
import CloseIcon from '@mui/icons-material/Close'

const APK_URL = '/app-debug.apk' // public 폴더 기준 최신 APK 경로

const Settings = () => {
  const [currentVersion, setCurrentVersion] = useState('로딩중...')
  const [latestVersion, setLatestVersion] = useState('로딩중...')
  const [isDownloading, setIsDownloading] = useState(false)
  const [downloadProgress, setDownloadProgress] = useState(0)
  const [showSnackbar, setShowSnackbar] = useState(false)
  const [snackbarMsg, setSnackbarMsg] = useState('')
  const [showUpdateDialog, setShowUpdateDialog] = useState(false)
  const [isError, setIsError] = useState(false)
  const downloadRef = useRef<HTMLAnchorElement | null>(null)

  useEffect(() => {
    fetch('/version.json')
      .then(res => res.json())
      .then(data => {
        setLatestVersion(data.latest)
        setCurrentVersion(data.current || '알 수 없음')
        if (data.latest && data.current && data.latest !== data.current) {
          setShowUpdateDialog(true)
        }
      })
      .catch(() => {
        setLatestVersion('연결 실패')
        setCurrentVersion('연결 실패')
        setIsError(true)
      })
  }, [])

  const isUpdateAvailable = currentVersion !== latestVersion && latestVersion !== '로딩중...'

  // 실제 다운로드 진행률 구현 (XHR 활용)
  const handleUpdate = () => {
    setIsDownloading(true)
    setDownloadProgress(0)
    setShowSnackbar(false)
    const xhr = new XMLHttpRequest()
    xhr.open('GET', APK_URL, true)
    xhr.responseType = 'blob'
    xhr.onprogress = (event) => {
      if (event.lengthComputable) {
        setDownloadProgress(Math.round((event.loaded / event.total) * 100))
      }
    }
    xhr.onload = () => {
      setIsDownloading(false)
      setDownloadProgress(100)
      setSnackbarMsg('다운로드 완료! 설치를 시작합니다.')
      setShowSnackbar(true)
      // 자동 설치 인텐트(안드로이드)
      const url = window.URL.createObjectURL(xhr.response)
      const a = document.createElement('a')
      a.href = url
      a.download = 'app-debug.apk'
      document.body.appendChild(a)
      a.click()
      setTimeout(() => {
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      }, 2000)
    }
    xhr.onerror = () => {
      setIsDownloading(false)
      setSnackbarMsg('다운로드 실패! 네트워크를 확인하세요.')
      setShowSnackbar(true)
    }
    xhr.send()
  }

  return (
    <Box sx={{ maxWidth: 480, mx: 'auto', mt: 6, p: 2 }}>
      <Fade in>
        <Card sx={{ borderRadius: 4, boxShadow: 6, p: 0, overflow: 'visible' }}>
          <CardContent sx={{ p: 4 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <SystemUpdateAltRoundedIcon sx={{ fontSize: 36, color: '#4F8CFF', mr: 1 }} />
              <Typography variant="h5" fontWeight={700}>앱 설정</Typography>
            </Box>
            <Divider sx={{ mb: 3 }} />
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle1" color="text.secondary">현재 버전</Typography>
              <Typography variant="h6" fontWeight={600}>{currentVersion}</Typography>
            </Box>
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" color="text.secondary">최신 버전</Typography>
              <Typography variant="h6" fontWeight={600}>{latestVersion}</Typography>
            </Box>
            {isError && (
              <Typography color="error" sx={{ mb: 2 }}>버전 정보를 불러오지 못했습니다. 네트워크를 확인하세요.</Typography>
            )}
            {isUpdateAvailable && !isError && (
              <Fade in>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <WarningAmberRoundedIcon sx={{ color: '#FFB300', mr: 1, fontSize: 28, animation: 'shake 0.7s infinite alternate' }} />
                  <Typography color="warning.main" fontWeight={600}>새 버전이 있습니다! 업데이트를 권장합니다.</Typography>
                  <style>{`@keyframes shake { 0% { transform: rotate(-5deg); } 100% { transform: rotate(5deg); }}`}</style>
                </Box>
              </Fade>
            )}
            {!isUpdateAvailable && !isError && (
              <Fade in>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <CheckCircleIcon sx={{ color: '#4CAF50', mr: 1, fontSize: 28, animation: 'pop 0.7s' }} />
                  <Typography color="success.main" fontWeight={600}>최신 버전입니다.</Typography>
                  <style>{`@keyframes pop { 0% { transform: scale(0.8); } 100% { transform: scale(1); }}`}</style>
                </Box>
              </Fade>
            )}
            {isDownloading && (
              <Box sx={{ mt: 3 }}>
                <LinearProgress variant="determinate" value={downloadProgress} sx={{ height: 10, borderRadius: 5 }} />
                <Typography sx={{ mt: 1, textAlign: 'center' }}>{downloadProgress}%</Typography>
              </Box>
            )}
            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
              {isUpdateAvailable && !isError && !isDownloading && (
                <Button
                  variant="contained"
                  color="primary"
                  size="large"
                  onClick={handleUpdate}
                  sx={{
                    borderRadius: 3,
                    boxShadow: 3,
                    px: 4,
                    py: 1.5,
                    fontWeight: 700,
                    fontSize: 18,
                    transition: 'all 0.2s',
                    '&:hover': {
                      background: 'linear-gradient(90deg, #4F8CFF 0%, #6FC3FF 100%)',
                      boxShadow: 6
                    }
                  }}
                >
                  업데이트
                </Button>
              )}
            </Box>
            <Typography variant="h4" color="primary" sx={{ mb: 2 }}>테스트 빌드: 2024-05-13</Typography>
          </CardContent>
        </Card>
      </Fade>
      {/* 새 버전 알림 모달 */}
      <Dialog open={showUpdateDialog && isUpdateAvailable && !isError} onClose={() => setShowUpdateDialog(false)}>
        <DialogTitle sx={{ display: 'flex', alignItems: 'center' }}>
          <WarningAmberRoundedIcon sx={{ color: '#FFB300', mr: 1 }} />
          새 버전이 있습니다!
          <IconButton onClick={() => setShowUpdateDialog(false)} sx={{ ml: 'auto' }}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          <Typography>최신 버전({latestVersion})으로 업데이트 하시겠습니까?</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowUpdateDialog(false)} color="inherit">나중에</Button>
          <Button onClick={() => { setShowUpdateDialog(false); handleUpdate() }} color="primary" variant="contained">업데이트</Button>
        </DialogActions>
      </Dialog>
      {/* 다운로드/설치 안내 스낵바 */}
      <Snackbar
        open={showSnackbar}
        autoHideDuration={3000}
        onClose={() => setShowSnackbar(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setShowSnackbar(false)} severity={downloadProgress === 100 ? 'success' : 'error'} sx={{ width: '100%' }}>
          {snackbarMsg}
        </Alert>
      </Snackbar>
    </Box>
  )
}

export default Settings 