//sign-in.js
//获取应用实例
const app = getApp()

Page({
  data: {
    mobile: null,
    password: null
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
        status = res.statusCode
        if (status === '201') {
          wx.redirectTo({
            url: '../demo/demo',
          })
        } else if (status === '400') {
          // TODO
          console.log(res.data.error)
        } else {
          // TODO
          console.log(res.data.error)
        }
      }
    })
    // wx.navigateTo({
    //   url: '../sign-up/sign-up',
    //   success: function(res) {},
    //   fail: function(res) {},
    //   complete: function(res) {},
    // })
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
