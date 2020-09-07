webpackHotUpdate("static/development/pages/index.js",{

/***/ "./pages/index.js":
/*!************************!*\
  !*** ./pages/index.js ***!
  \************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var _babel_runtime_regenerator__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime/regenerator */ \"./node_modules/@babel/runtime/regenerator/index.js\");\n/* harmony import */ var _babel_runtime_regenerator__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_regenerator__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _babel_runtime_helpers_esm_asyncToGenerator__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @babel/runtime/helpers/esm/asyncToGenerator */ \"./node_modules/@babel/runtime/helpers/esm/asyncToGenerator.js\");\n/* harmony import */ var _babel_runtime_helpers_esm_classCallCheck__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @babel/runtime/helpers/esm/classCallCheck */ \"./node_modules/@babel/runtime/helpers/esm/classCallCheck.js\");\n/* harmony import */ var _babel_runtime_helpers_esm_createClass__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @babel/runtime/helpers/esm/createClass */ \"./node_modules/@babel/runtime/helpers/esm/createClass.js\");\n/* harmony import */ var _babel_runtime_helpers_esm_inherits__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @babel/runtime/helpers/esm/inherits */ \"./node_modules/@babel/runtime/helpers/esm/inherits.js\");\n/* harmony import */ var _babel_runtime_helpers_esm_possibleConstructorReturn__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @babel/runtime/helpers/esm/possibleConstructorReturn */ \"./node_modules/@babel/runtime/helpers/esm/possibleConstructorReturn.js\");\n/* harmony import */ var _babel_runtime_helpers_esm_getPrototypeOf__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @babel/runtime/helpers/esm/getPrototypeOf */ \"./node_modules/@babel/runtime/helpers/esm/getPrototypeOf.js\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! react */ \"./node_modules/react/index.js\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_7__);\n/* harmony import */ var next_link__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! next/link */ \"./node_modules/next/link.js\");\n/* harmony import */ var next_link__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(next_link__WEBPACK_IMPORTED_MODULE_8__);\n/* harmony import */ var next_router__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! next/router */ \"./node_modules/next/dist/client/router.js\");\n/* harmony import */ var next_router__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(next_router__WEBPACK_IMPORTED_MODULE_9__);\n\n\n\n\n\n\n\nvar _jsxFileName = \"/Users/shubmeister/Desktop/ReactUdemy/NextJS/pages/index.js\";\nvar __jsx = react__WEBPACK_IMPORTED_MODULE_7___default.a.createElement;\n\nfunction _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = Object(_babel_runtime_helpers_esm_getPrototypeOf__WEBPACK_IMPORTED_MODULE_6__[\"default\"])(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = Object(_babel_runtime_helpers_esm_getPrototypeOf__WEBPACK_IMPORTED_MODULE_6__[\"default\"])(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return Object(_babel_runtime_helpers_esm_possibleConstructorReturn__WEBPACK_IMPORTED_MODULE_5__[\"default\"])(this, result); }; }\n\nfunction _isNativeReflectConstruct() { if (typeof Reflect === \"undefined\" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === \"function\") return true; try { Date.prototype.toString.call(Reflect.construct(Date, [], function () {})); return true; } catch (e) { return false; } }\n\n\n\n\n/**\n * Just setting up a folder structure creates URLs and pages, and they are all rendered server-side. No need\n * for routing at all. There's also automatic code splitting since this is all rendered server side. \n * You cannot use CSS modules if using NextJs, but you can use styled jsx instead.. \n * This isn't a normal lifecycle hook, as it is static and can be called without the component being \n * instantiated. It executes first on the server, so you could do the pre-populating of props from a \n * database or whatever.\n */\n\nvar IndexPage = /*#__PURE__*/function (_Component) {\n  Object(_babel_runtime_helpers_esm_inherits__WEBPACK_IMPORTED_MODULE_4__[\"default\"])(IndexPage, _Component);\n\n  var _super = _createSuper(IndexPage);\n\n  function IndexPage() {\n    Object(_babel_runtime_helpers_esm_classCallCheck__WEBPACK_IMPORTED_MODULE_2__[\"default\"])(this, IndexPage);\n\n    return _super.apply(this, arguments);\n  }\n\n  Object(_babel_runtime_helpers_esm_createClass__WEBPACK_IMPORTED_MODULE_3__[\"default\"])(IndexPage, [{\n    key: \"render\",\n    value: function render() {\n      return __jsx(\"div\", {\n        __self: this,\n        __source: {\n          fileName: _jsxFileName,\n          lineNumber: 20,\n          columnNumber: 16\n        }\n      }, __jsx(\"h1\", {\n        __self: this,\n        __source: {\n          fileName: _jsxFileName,\n          lineNumber: 21,\n          columnNumber: 13\n        }\n      }, \"The main page\"), __jsx(\"p\", {\n        __self: this,\n        __source: {\n          fileName: _jsxFileName,\n          lineNumber: 22,\n          columnNumber: 13\n        }\n      }, \"Go to \", __jsx(next_link__WEBPACK_IMPORTED_MODULE_8___default.a, {\n        href: \"/auth\",\n        __self: this,\n        __source: {\n          fileName: _jsxFileName,\n          lineNumber: 22,\n          columnNumber: 22\n        }\n      }, __jsx(\"a\", {\n        __self: this,\n        __source: {\n          fileName: _jsxFileName,\n          lineNumber: 22,\n          columnNumber: 41\n        }\n      }, \"Auth\"))), __jsx(\"button\", {\n        onClick: function onClick() {\n          return next_router__WEBPACK_IMPORTED_MODULE_9___default.a.push(\"/auth\");\n        },\n        __self: this,\n        __source: {\n          fileName: _jsxFileName,\n          lineNumber: 23,\n          columnNumber: 13\n        }\n      }, \"Go to Auth\"));\n    }\n  }], [{\n    key: \"getInitialProps\",\n    value: function () {\n      var _getInitialProps = Object(_babel_runtime_helpers_esm_asyncToGenerator__WEBPACK_IMPORTED_MODULE_1__[\"default\"])( /*#__PURE__*/_babel_runtime_regenerator__WEBPACK_IMPORTED_MODULE_0___default.a.mark(function _callee(context) {\n        return _babel_runtime_regenerator__WEBPACK_IMPORTED_MODULE_0___default.a.wrap(function _callee$(_context) {\n          while (1) {\n            switch (_context.prev = _context.next) {\n              case 0:\n                console.log(context);\n                return _context.abrupt(\"return\", {\n                  appName: 'Super App'\n                });\n\n              case 2:\n              case \"end\":\n                return _context.stop();\n            }\n          }\n        }, _callee);\n      }));\n\n      function getInitialProps(_x) {\n        return _getInitialProps.apply(this, arguments);\n      }\n\n      return getInitialProps;\n    }()\n  }]);\n\n  return IndexPage;\n}(react__WEBPACK_IMPORTED_MODULE_7__[\"Component\"]);\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (IndexPage);\n\n;\n    var _a, _b;\n    // Legacy CSS implementations will `eval` browser code in a Node.js context\n    // to extract CSS. For backwards compatibility, we need to check we're in a\n    // browser context before continuing.\n    if (typeof self !== 'undefined' &&\n        // AMP / No-JS mode does not inject these helpers:\n        '$RefreshHelpers$' in self) {\n        var currentExports_1 = module.__proto__.exports;\n        var prevExports = (_b = (_a = module.hot.data) === null || _a === void 0 ? void 0 : _a.prevExports) !== null && _b !== void 0 ? _b : null;\n        // This cannot happen in MainTemplate because the exports mismatch between\n        // templating and execution.\n        self.$RefreshHelpers$.registerExportsForReactRefresh(currentExports_1, module.i);\n        // A module can be accepted automatically based on its exports, e.g. when\n        // it is a Refresh Boundary.\n        if (self.$RefreshHelpers$.isReactRefreshBoundary(currentExports_1)) {\n            // Save the previous exports on update so we can compare the boundary\n            // signatures.\n            module.hot.dispose(function (data) {\n                data.prevExports = currentExports_1;\n            });\n            // Unconditionally accept an update to this module, we'll check if it's\n            // still a Refresh Boundary later.\n            module.hot.accept();\n            // This field is set when the previous version of this module was a\n            // Refresh Boundary, letting us know we need to check for invalidation or\n            // enqueue an update.\n            if (prevExports !== null) {\n                // A boundary can become ineligible if its exports are incompatible\n                // with the previous exports.\n                //\n                // For example, if you add/remove/change exports, we'll want to\n                // re-execute the importing modules, and force those components to\n                // re-render. Similarly, if you convert a class component to a\n                // function, we want to invalidate the boundary.\n                if (self.$RefreshHelpers$.shouldInvalidateReactRefreshBoundary(prevExports, currentExports_1)) {\n                    module.hot.invalidate();\n                }\n                else {\n                    self.$RefreshHelpers$.scheduleUpdate();\n                }\n            }\n        }\n        else {\n            // Since we just executed the code for the module, it's possible that the\n            // new exports made it ineligible for being a boundary.\n            // We only care about the case when we were _previously_ a boundary,\n            // because we already accepted this update (accidental side effect).\n            var isNoLongerABoundary = prevExports !== null;\n            if (isNoLongerABoundary) {\n                module.hot.invalidate();\n            }\n        }\n    }\n\n/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./../node_modules/webpack/buildin/harmony-module.js */ \"./node_modules/webpack/buildin/harmony-module.js\")(module)))//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vLi9wYWdlcy9pbmRleC5qcz80NGQ4Il0sIm5hbWVzIjpbIkluZGV4UGFnZSIsIlJvdXRlciIsInB1c2giLCJjb250ZXh0IiwiY29uc29sZSIsImxvZyIsImFwcE5hbWUiLCJDb21wb25lbnQiXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBRUE7Ozs7Ozs7OztJQVFNQSxTOzs7Ozs7Ozs7Ozs7OzZCQU1PO0FBQ0wsYUFBTztBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBLFNBQ0g7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQSx5QkFERyxFQUVIO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUEsbUJBQVMsTUFBQyxnREFBRDtBQUFNLFlBQUksRUFBQyxPQUFYO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUEsU0FBbUI7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQSxnQkFBbkIsQ0FBVCxDQUZHLEVBR0g7QUFBUSxlQUFPLEVBQUU7QUFBQSxpQkFBTUMsa0RBQU0sQ0FBQ0MsSUFBUCxDQUFZLE9BQVosQ0FBTjtBQUFBLFNBQWpCO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUEsc0JBSEcsQ0FBUDtBQUtIOzs7OytOQVg0QkMsTzs7Ozs7QUFDekJDLHVCQUFPLENBQUNDLEdBQVIsQ0FBWUYsT0FBWjtpREFDTztBQUFDRyx5QkFBTyxFQUFFO0FBQVYsaUI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7RUFIU0MsK0M7O0FBZVRQLHdFQUFmIiwiZmlsZSI6Ii4vcGFnZXMvaW5kZXguanMuanMiLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QsIHsgQ29tcG9uZW50IH0gZnJvbSAncmVhY3QnXG5pbXBvcnQgTGluayBmcm9tICduZXh0L2xpbmsnXG5pbXBvcnQgUm91dGVyIGZyb20gJ25leHQvcm91dGVyJ1xuXG4vKipcbiAqIEp1c3Qgc2V0dGluZyB1cCBhIGZvbGRlciBzdHJ1Y3R1cmUgY3JlYXRlcyBVUkxzIGFuZCBwYWdlcywgYW5kIHRoZXkgYXJlIGFsbCByZW5kZXJlZCBzZXJ2ZXItc2lkZS4gTm8gbmVlZFxuICogZm9yIHJvdXRpbmcgYXQgYWxsLiBUaGVyZSdzIGFsc28gYXV0b21hdGljIGNvZGUgc3BsaXR0aW5nIHNpbmNlIHRoaXMgaXMgYWxsIHJlbmRlcmVkIHNlcnZlciBzaWRlLiBcbiAqIFlvdSBjYW5ub3QgdXNlIENTUyBtb2R1bGVzIGlmIHVzaW5nIE5leHRKcywgYnV0IHlvdSBjYW4gdXNlIHN0eWxlZCBqc3ggaW5zdGVhZC4uIFxuICogVGhpcyBpc24ndCBhIG5vcm1hbCBsaWZlY3ljbGUgaG9vaywgYXMgaXQgaXMgc3RhdGljIGFuZCBjYW4gYmUgY2FsbGVkIHdpdGhvdXQgdGhlIGNvbXBvbmVudCBiZWluZyBcbiAqIGluc3RhbnRpYXRlZC4gSXQgZXhlY3V0ZXMgZmlyc3Qgb24gdGhlIHNlcnZlciwgc28geW91IGNvdWxkIGRvIHRoZSBwcmUtcG9wdWxhdGluZyBvZiBwcm9wcyBmcm9tIGEgXG4gKiBkYXRhYmFzZSBvciB3aGF0ZXZlci5cbiAqL1xuY2xhc3MgSW5kZXhQYWdlIGV4dGVuZHMgQ29tcG9uZW50IHtcbiAgICBzdGF0aWMgYXN5bmMgZ2V0SW5pdGlhbFByb3BzKGNvbnRleHQpIHtcbiAgICAgICAgY29uc29sZS5sb2coY29udGV4dClcbiAgICAgICAgcmV0dXJuIHthcHBOYW1lOiAnU3VwZXIgQXBwJ31cbiAgICB9XG5cbiAgICByZW5kZXIoKSB7XG4gICAgICAgIHJldHVybiA8ZGl2PlxuICAgICAgICAgICAgPGgxPlRoZSBtYWluIHBhZ2U8L2gxPlxuICAgICAgICAgICAgPHA+R28gdG8gPExpbmsgaHJlZj1cIi9hdXRoXCI+PGE+QXV0aDwvYT48L0xpbms+PC9wPlxuICAgICAgICAgICAgPGJ1dHRvbiBvbkNsaWNrPXsoKSA9PiBSb3V0ZXIucHVzaChcIi9hdXRoXCIpfT5HbyB0byBBdXRoPC9idXR0b24+XG4gICAgICAgIDwvZGl2PlxuICAgIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgSW5kZXhQYWdlIl0sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///./pages/index.js\n");

/***/ })

})