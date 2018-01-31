// pages/transactions/transactions.js
const app = getApp()
var status = require('../../utils/error.js')

Page({

  data: {
    orders: null
  },

  onLoad: function (options) {
    this.getOrders
    ()
  },

  getOrders: function () {
    var that = this
    wx.request({
      url: 'http://localhost:10000/gateway/users/' + app.globalData.userId + '/orders',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      success: function(res) {
        if (res.statusCode === 200) {
          var orders = res.data.orders
          for (var order of orders) {
            order['createdDate'] = new Date(order.createdDate).toLocaleString()
          }
          that.setData({
            orders: res.data.orders
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
  
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
  
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  }
})