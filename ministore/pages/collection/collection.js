// pages/collection/collection.js
const app = getApp()
var status = require('../../utils/error.js')
var QRCode = require('../../utils/qrcode.js')
var util = require('../../utils/util.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    code: null,
    wechatInfo: null
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    wx.getSystemInfo({
      success: function(res) {
        that.setData({
          windowWidth: res.windowWidth,
          windowHeight: res.windowHeight
        })
      }
    })
    this.getQRCodeInfo()
    console.log(that.data)
  },

  getQRCodeInfo: function () {
    var that = this
    wx.request({
      url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/qr-code',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function (res) {
        if (res.statusCode === 200) {
          that.setData({
            code: res.data.code,
            wechatInfo: res.data.wechatInfo
          })
          var storeCode = that.createQRCode('storeCode', that.data.code)
          var wechatCode = that.createQRCode('wechatCode', that.data.wechatInfo)
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  createQRCode: function (canvasId, text) {
    return new QRCode(canvasId, {
      text: text,
      width: this.data.windowWidth / 2,
      height: this.data.windowWidth / 2,
      colorDark: "black",
      colorLight: "white",
      correctLevel: QRCode.CorrectLevel.H
    })
  },

  bindQRCode: function (e) {
    var that = this
    wx.scanCode({
      scanType: ['qrCode'],
      success: function (res) {
        var code = res.result
        wx.request({
          url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/bind-qr-code',
          header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
          method: 'POST',
          data: { QRCode: code },
          success: function (res) {
            if (res.statusCode === 201) {
              wx.showToast({
                title: '绑定成功',
              })
              that.onLoad()
            } else if (res.statusCode === 400) {
              status.status400(res.data.error)
            } else {
              status.status500()
            }
          }
        })
      }
    })
  },

  bindWechatCode: function (e) {
    var that = this
    wx.scanCode({
      scanType: ['qrCode'],
      success: function (res) {
        var wechatInfo = res.result
        wx.request({
          url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/bind-payment-info',
          header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
          method: 'POST',
          data: { wechatInfo: wechatInfo },
          success: function (res) {
            if (res.statusCode === 201) {
              wx.showToast({
                title: '绑定成功',
              })
              that.onLoad()
            } else if (res.statusCode === 400) {
              status.status400(res.data.error)
            } else {
              status.status500()
            }
          }
        })
      }
    })
  },

  savaStoreCode: function() {
    this.savaPic('storeCode')
  },

  savaPic: function(canvasId) {
    let that = this
    wx.canvasToTempFilePath({
      canvasId: canvasId,
      success: function(res) {
        util.savePicToAlbum(res.tempFilePath)
      }
    })
  }
})