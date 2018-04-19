//index.js
//获取应用实例
const app = getApp()
var status = require('../../utils/error.js')

Page({
  data: {
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
  },

  onLoad: function (options) {
    var scene = app.globalData.scene  // 场景值
    var code = decodeURIComponent(options.scene) // 扫码得到的内容
    app.globalData.code = code
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse) {
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        app.globalData.userInfo = res.userInfo
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
    if (scene == 1047) {
      wx.redirectTo({
        url: '../payment/payment',
      })
    }
  },


  // getUserInfo: function (e) {
  //   // console.log(e)
  //   app.globalData.userInfo = e.detail.userInfo
  //   this.setData({
  //     userInfo: e.detail.userInfo,
  //     hasUserInfo: true
  //   })
  // },

  // scanQRCode: function (e) {
  //   var that = this
  //   wx.scanCode({
  //     scanType: ['qrCode'],
  //     success: function (res) {
  //       wx.navigateTo({
  //         url: '../payment/payment',
  //       })
  //     }
  //   })
  // },

  relogin: function () {
    var that = this;
    app.globalData.token = null;
    app.registerUser();
    wx.showToast({
      title: '重新登录成功',
      success: function (res) {
        if (res.confirm) {
          that.onShow();
        }
      }
    })
  },
})
