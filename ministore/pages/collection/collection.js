// pages/collection/collection.js
const app = getApp()
var status = require('../../utils/error.js')
var QRCode = require('../../utils/qrcode.js')
var util = require('../../utils/util.js')

Page({

  data: {
    code: null,
    wechatInfo: null,
    hasPointPassword: false,
    changingPassword: false,
    settingPassword: false
  },

  onLoad: function (options) {
    // console.log(this.data)
    var that = this
    wx.getSystemInfo({
      success: function (res) {
        that.setData({
          windowWidth: res.windowWidth,
          windowHeight: res.windowHeight
        })
      }
    })
    this.getQRCodeInfo()
    this.getPointPassword()
  },

  getPointPassword: function () {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/point-password',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function (res) {
        if (res.statusCode === 200) {
          if (Object.keys(res.data).length != 0) {
            var password = res.data.pointPassword
            if (password != undefined && password != '') {
              that.setData({
                hasPointPassword: true
              })
            }
          }
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  pointPassword: function (e) {
    this.setData({
      pointPassword: e.detail.value
    })
  },

  changePointPassword: function () {
    this.setData({
      changingPassword: true
    })
  },

  changePointPasswordDetermine: function () {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/point-password',
      method: 'PUT',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      data: { pointPassword: that.data.pointPassword },
      success: function (res) {
        if (res.statusCode === 200) {
          wx.showToast({
            title: '修改成功',
          })
          that.setData({
            changingPassword: false
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  changePointPasswordCancel: function () {
    this.setData({
      changingPassword: false
    })
  },

  setPointPassword: function () {
    this.setData({
      settingPassword: true
    })
  },

  setPointPasswordDetermine: function () {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/point-password',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      method: 'POST',
      data: { pointPassword: that.data.pointPassword },
      success: function (res) {
        if (res.statusCode === 201) {
          wx.showToast({
            title: '设置成功',
          })
          that.setData({
            settingPassword: false,
            hasPointPassword: true
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  setPointPasswordCancel: function () {
    this.setData({
      settingPassword: false
    })
  },

  getQRCodeInfo: function () {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/qr-code',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function (res) {
        if (res.statusCode === 200) {
          if (Object.keys(res.data).length !== 0) {
            // 这里的code应该是用原始的scene通过API生成的个人版的二维码
            // 个人版上线后修改
            that.setData({
              code: res.data.code,
              wechatInfo: res.data.wechatInfo
            })
            that.createQRCode('storeCode', that.data.code)
            that.createQRCode('wechatCode', that.data.wechatInfo)
          }
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

  storeCode: function (e) {
    this.setData({
      codeInput: e.detail.value
    })
  },

  bindStoreCode: function (e) {
    var that = this
    var codeInput = this.data.codeInput
    wx.request({
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/bind-qr-code',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      method: 'POST',
      data: { QRCode: codeInput },
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
  },

  // bindWechatCode: function (e) {
  //   var that = this
  //   wx.scanCode({
  //     scanType: ['qrCode'],
  //     success: function (res) {
  //       var wechatInfo = res.result
  //       wx.request({
  //         url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/bind-payment-info',
  //         header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
  //         method: 'POST',
  //         data: { wechatInfo: wechatInfo },
  //         success: function (res) {
  //           if (res.statusCode === 201) {
  //             wx.showToast({
  //               title: '绑定成功',
  //             })
  //             that.onLoad()
  //           } else if (res.statusCode === 400) {
  //             status.status400(res.data.error)
  //           } else {
  //             status.status500()
  //           }
  //         }
  //       })
  //     }
  //   })
  // },

  saveStoreCode: function () {
    this.savaPic('storeCode')
  },

  savaPic: function (canvasId) {
    let that = this
    wx.canvasToTempFilePath({
      canvasId: canvasId,
      success: function (res) {
        util.savePicToAlbum(res.tempFilePath)
      }
    })
  }
})