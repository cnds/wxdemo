// pages/reset-pwd/reset-pwd.js
var status = require('../../utils/error.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    mobile: null,
    newPassword: null,
    newPassword2: null,
    code: null,
  },
  resetPwdClick: function (event) {
    if (this.data.newPassword != this.data.newPassword2) {
      wx.showModal({
        title: '提示',
        content: '两次输入的密码不一致，请重新输入',
        showCancel: false
      })
      return;
    }
    wx.request({
      url: 'http://localhost:20000/authorization/stores/reset-password',
      data: {
        mobile: this.data.mobile,
        newPassword: this.data.newPassword,
        code: this.data.code
      },
      method: 'POST',
      success: function (res) {
        status = res.statusCode
        if (status === '201') {
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
  mobileInput: function (event) {
    this.setData({
      mobile: event.detail.value
    })
  },
  passwordInput: function (event) {
    this.setData({
      newPassword: event.detail.value
    })
  },

  passwordInput2: function(event) {
    this.setData({
      newPassword2: event.detail.value
    })
  },

  smsInput: function (event) {
    this.setData({
      code: event.detail.value
    })
  },
  sendSmsClick: function (event) {
    wx.request({
      url: 'http://localhost:20000/authorization/sms',
      data: {
        verifyType: 'store_reset_password',
        mobile: this.data.mobile
      },
      method: 'POST',
      success: function (res) {
        if (res.statusCode !== 201) {
          if (res.statusCode === 400) {
            status.status400(res.data.error)
          } else {
            status.status500()
          }
        }
      }
    })
  }
})