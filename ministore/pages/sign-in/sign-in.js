//sign-in.js
//获取应用实例
const app = getApp()
var status = require('../../utils/error.js')

Page({
  data: {
    mobile: null,
    password: null
  },

  onLoad: function() {
    var storeInfo = wx.getStorageSync('storeInfo')
    if (storeInfo) {
      app.globalData.storeInfo = storeInfo
      wx.redirectTo({
        url: '../index/index',
      })
    }
  },

  //事件处理函数
  loginClick: function() {
    wx.request({
      url: 'http://localhost:20000/authorization/store-sessions',
      method: 'POST',
      data: {
        mobile: this.data.mobile,
        password: this.data.password
      },
      success: function(res) {
        if (res.statusCode === 201) {
          app.globalData.storeInfo = res.data
          wx.setStorage({
            key: 'storeInfo',
            data: res.data,
          })
          wx.redirectTo({
            url: '../index/index',
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  mobileInput: function(event) {
    this.setData({
      mobile: event.detail.value
    })
  },

  passwordInput: function(event) {
    this.setData({
      password: event.detail.value
    })
  },

  signUpTap: function(event) {
    wx.navigateTo({
      url: '../sign-up/sign-up',
    })
  },

  ResetPwdTap: function(event) {
    wx.navigateTo({
      url: '../reset-pwd/reset-pwd',
    })
  }
})
