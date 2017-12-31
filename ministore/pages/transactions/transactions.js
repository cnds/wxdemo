// pages/transactions/transactions.js
const app = getApp()
var time = require('../../utils/util.js')

Page({
  data: {
    orders: null
  },
  transactionClick: function(event) {
    console.log(event)
  },
  onLoad: function(event) {
    var that = this
    console.log(app.globalData.storeInfo.token)
    wx.request({
      url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/orders',
      header: {'Authorization': 'Bearer ' + app.globalData.storeInfo.token},
      success: function(res) {
        if (res.statusCode === 200) {
          var orders = res.data.orders
          for (var order of orders) {
            order['createdDate'] = new Date(order.createdDate).toLocaleString()
          }
          that.setData({
            orders: orders
          })
        } else if (res.statusCode === 400) {
          wx.showModal({
            title: '错误',
            content: res.data.error,
            showCancel: false
          })
        } else {
          wx.showModal({
            title: '错误',
            content: '服务器内部错误',
            showCancel: false
          })
        }
      }
    })
  }
})