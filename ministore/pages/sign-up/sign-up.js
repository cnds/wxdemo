// pages/sign-up/sign-up.js
const app = getApp()
var status = require('../../utils/error.js')
Page({

  data: {
    mobile: null,
    password: null,
    smsCode: null,
    address: null,
    storeName: null
  },
  signupClick: function(event) {
    wx.request({
      url: app.globalData.config.authorization + '/stores',
      data: {
        mobile: this.data.mobile,
        password: this.data.password,
        smsCode: this.data.smsCode,
        address: this.data.address,
        storeName: this.data.storeName
      },
      method: 'POST',
      success: function(res) {
        if (res.statusCode === 201) {
          wx.redirectTo({
            url: '../sign-in/sign-in',
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
  smsInput: function(event) {
    this.setData({
      smsCode: event.detail.value
    })
  },
  sendSmsClick: function(event) {
    wx.request({
      url: app.globalData.config.authorization + '/sms',
      data: {
        verifyType: 'store_sign_up',
        mobile: this.data.mobile
      },
      method: 'POST',
      success: function(res) {
        if (res.statusCode !== 201) {
          if (res.statusCode === 400) {
            status.status400(res.data.error)
          } else {
            status.status500()
          }
        }
      }
    })
  },

  storeNameInput: function(event) {
    this.setData({
      storeName: event.detail.value
    })
  },

  addressInput: function(event) {
    this.setData({
      address: event.detail.value
    })
  }

})