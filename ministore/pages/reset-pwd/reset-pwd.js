// pages/reset-pwd/reset-pwd.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    mobile: null,
    newPassword: null,
    code: null,
  },
  resetPwdClick: function (event) {
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
        } else {
          console.log(res.data.error)
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
        status = res.statusCode
        if (status !== '201') {
          console.log(res.data.error)
        }
      }
    })
  }

})