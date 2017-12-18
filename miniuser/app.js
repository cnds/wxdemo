//app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    this.registerUser()
  },

  login: function (openid) {
    wx.request({
      url: 'http://localhost:20000/authorizatin/user-sessions',
      data: {openid: openid},
      method: 'POST',
      success: function(res) {
        if (res.statusCode === 201) {
          app.globalData.token = res.data.token
        } else {
          console.log(res)
          return;
        }
      }
    })
  },

  registerUser: function () {
    var that = this
    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        var code = res.code
        console.log(code)
        wx.getSetting({
          success: res => {
            if (res.authSetting['scope.userInfo']) {
              // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
              wx.getUserInfo({
                success: res => {
                  // 可以将 res 发送给后台解码出 unionId
                  this.globalData.userInfo = res.userInfo
                  console.log(res)

                  wx.request({
                    url: 'http://localhost:20000/authorization/users/register-status',
                    data: {
                      code: code
                    },
                    method: 'POST',
                    success: function (res) {
                      if (res.statusCode === 201) {
                        that.login(res.data.openid)
                      } else {
                        var iv = res.iv
                        var encryptedData = res.encryptedData
                        wx.request({
                          url: 'http://localhost:20000/authorization/users',
                          data: { code: code, iv: iv, encryptedData: encryptedData },
                          method: 'POST',
                          success: function (res) {
                            wx.hideLoading();
                            that.login(res.data.openId);
                            // console.log(res)
                          }
                        })
                      }
                    }
                  })
                  // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
                  // 所以此处加入 callback 以防止这种情况
                  if (this.userInfoReadyCallback) {
                    this.userInfoReadyCallback(res)
                  }
                }
              })
            }
          }
        })
      }
    })
  },
  globalData: {
    userInfo: null,
    token: null
  }
})
