// pages/sign-up/sign-up.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    mobile: null,
    password: null,
    smsCode: null,
    address: null,
    storeName: null
  },
  signupClick: function(event) {
    wx.request({
      url: 'http://localhost:20000/authorization/stores',
      data: {
        mobile: this.data.mobile,
        password: this.data.password,
        smsCode: this.data.smsCode,
        address: this.data.address,
        storeName: this.data.storeName
      },
      method: 'POST',
      success: function(res) {
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
      url: 'http://localhost:20000/authorization/sms',
      data: {
        verifyType: 'store_sign_up',
        mobile: this.data.mobile
      },
      method: 'POST',
      success: function(res) {
        status = res.statusCode
        if (status !== '201') {
          console.log(res.data.error)
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