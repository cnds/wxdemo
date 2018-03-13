// pages/index/index.js
var status = require('../../utils/error.js')
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
    var that = this
    wx.scanCode({
      scanType: ['qrCode'],
      success: function (res) {
        console.log(res)
        // var scene = decodeURIComponent(res.scene)
        var scene = 'testqrcode'
        // 传入商铺的id和支付信息
        wx.request({
          url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/bind-qr-code',
          method: 'POST',
          header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
          data: { QRCode: scene },
          success: function (res) {
            if (res.statusCode === 201) {
              wx.showActionSheet({
                itemList: ['继续绑定收款码', '下次再说'],
                success: function (res) {
                  if (res.tapIndex === 0) {
                    that.bindCollectCode()
                  } else if (res.tapIndex === 1) {
                    console.log(res)
                  }
                }
              })
            } else if (res.statusCode === 400) {
              if (res.data.error === 'QR_CODE_ALREADY_BEEN_BOUND') {
                wx.showActionSheet({
                  itemList: ['继续绑定收款码', '下次再说'],
                  success: function(res) {
                    if (res.tapIndex === 0) {
                      that.bindCollectCode()
                    } else if (res.tapIndex === 1) {
                      console.log(res)
                    }
                  }
                })
              } else {
              status.status400(res.data.error)
              }
            } else {
              status.status500()
            }
          }
        })
      }
    })
  },

  bindCollectCode: function(e) {
    wx.scanCode({
      scanType: ['qrCode'],
      success: function (res) {
        console.log(res)
        var wechatInfo = res.result
        wx.request({
          url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/bind-collect-code',
          method: 'POST',
          data: { WechatInfo: wechatInfo },
          success: function (res) {
            if (res.statusCode === 201) {
              wx.showToast({
                title: '绑定收款码成功'
              })
            } else if (res.statusCode === 400) {
              status.status400(res.data.error)
            } else {
              status.status500()
            }
          }
        })
      }
    })
  }
})