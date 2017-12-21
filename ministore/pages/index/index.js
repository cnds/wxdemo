// pages/index/index.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    storeInfo: {}
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      storeInfo: app.globalData.storeInfo
    })
  },

  bindQRCode: function(e) {
    wx.scanCode({
      scanType: ['qrCode'],
      success: function(res) {
        console.log(res)
      }
    })
  }

  
})