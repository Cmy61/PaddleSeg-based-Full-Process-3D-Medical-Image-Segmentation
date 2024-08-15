export function _throttle(fn, interval = 200) {
  var _self = fn, // 保存需要被延迟执行的函数引用
    timer, // 定时器
    firstTime = true; // 是否是第一次调用
  return function () {
    var args = arguments;
    var _me = this;
    if (firstTime) { // 如果是第一次调用不需要延迟
      _self.apply(_me, args); // 执行fn函数并且修正此函数中this所运行的上下文指向
      return firstTime = false;
    }
    if (timer) { // 如果定时器还在，说明前一次延迟执行还没有完成
      return false;
    }
    timer = setTimeout(function () { // 延迟一段时间执行
      clearTimeout(timer);
      timer = null;
      _self.apply(_me, args); // 执行fn函数并且修正此函数中this所运行的上下文指向
    }, interval || 500);
  }
}