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

  bindQRCode: function (e) {
    wx.scanCode({
      scanType: ['qrCode'],
      success: function (res) {
        // var scene = decodeURIComponent(res.scene)
        var scene = 'T001'
        // 传入商铺的id和支付信息
        wx.request({
          url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/bind-qr-code',
          method: 'POST',
          data: { scene: scene, storeId: app.globalData.storeInfo.id },
          success: function (res) {
            console.log(res)
          }
        })
      }
    })
  }
})