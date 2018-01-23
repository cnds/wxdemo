// pages/profile/profile.js
const app = getApp()
var status = require('../../utils/error.js')

Page({
  data: {
    modifyProfile: false,
    storeName: null,
    address: null,
    storeId: null,
    mobile: null,
  },

  onLoad: function () {
    this.setData({
      storeName: app.globalData.storeInfo.storeName,
      storeId: app.globalData.storeInfo.id,
      mobile: app.globalData.storeInfo.mobile,
      address: app.globalData.storeInfo.address,
    })
  },

  modifyProfile: function () {
    this.setData({
      modifyProfile: true
    })
  },

  storeNameInput: function (e) {
    this.setData({
      storeName: e.detail.value
    })
  },

  addressInput: function (e) {
    this.setData({
      address: e.detail.value
    })
  },

  determine: function () {
    var that = this
    wx.request({
      url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id,
      data: { address: this.data.address, storeName: this.data.storeName },
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      method: 'PUT',
      success: function (res) {
        if (res.statusCode === 200) {
          that.setData({
            modifyProfile: false
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  cancel: function () {
    this.setData({
      modifyProfile: false
    })
  }
})