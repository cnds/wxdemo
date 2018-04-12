//app.js
const config = require('./utils/config.js')


App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    this.registerUser()
  },

  onShow: function (options) {
    this.globalData.scene = options.scene
  },

  login: function (openId) {
    var that = this
    wx.request({
      url: config.config.authorization + '/user-sessions',
      data: { openId: openId },
      method: 'POST',
      success: function (res) {
        if (res.statusCode === 201) {
          that.globalData.token = res.data.token
          that.globalData.userId = res.data.id
          wx.showToast({
            title: '登录成功',
          })
        } else {
          wx.showModal({
            title: '错误',
            content: '登录失败',
            showCancel: false
          })
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
        // console.log(res)
        wx.getSetting({
          success: res => {
            // console.log(res)
            wx.getUserInfo({
              success: res => {
                // 可以将 res 发送给后台解码出 unionId
                this.globalData.userInfo = res.userInfo
                // console.log(res)
                var iv = res.iv
                var encryptedData = res.encryptedData

                // 查看用户注册状态，如果未注册，创建用户后登录，如已注册则直接登录
                wx.request({
                  url: config.config.authorization + '/users/register-status',
                  data: { code: code },
                  method: 'POST',
                  success: function (res) {
                    if (res.statusCode === 201) {
                      that.login(res.data.openId)
                    } else if (res.statusCode === 400) {
                      wx.login({
                        success: res => {
                          var code = res.code
                          wx.request({
                            url: config.config.authorization + '/users',
                            data: {
                              code: code,
                              iv: iv,
                              encryptedData: encryptedData
                            },
                            method: 'POST',
                            success: function (res) {
                              wx.hideLoading();
                              that.login(res.data.id);
                            }
                          })
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
        })
      }
    })
  },

  globalData: {
    userInfo: null,
    token: null,
    userId: null,
    config: config.config
  }
})
