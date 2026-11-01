/*! Zdog (c) Metafizzy, MIT. glfx.js (c) 2011 Evan Wallace, MIT. VFX-JS (c) 2020-present The VFX-JS developers, MIT. Textos en LICENCIAS.md */
(() => {
  var __create = Object.create;
  var __defProp = Object.defineProperty;
  var __defProps = Object.defineProperties;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropDescs = Object.getOwnPropertyDescriptors;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __getOwnPropSymbols = Object.getOwnPropertySymbols;
  var __getProtoOf = Object.getPrototypeOf;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __propIsEnum = Object.prototype.propertyIsEnumerable;
  var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
  var __spreadValues = (a, b) => {
    for (var prop in b || (b = {}))
      if (__hasOwnProp.call(b, prop))
        __defNormalProp(a, prop, b[prop]);
    if (__getOwnPropSymbols)
      for (var prop of __getOwnPropSymbols(b)) {
        if (__propIsEnum.call(b, prop))
          __defNormalProp(a, prop, b[prop]);
      }
    return a;
  };
  var __spreadProps = (a, b) => __defProps(a, __getOwnPropDescs(b));
  var __objRest = (source, exclude) => {
    var target = {};
    for (var prop in source)
      if (__hasOwnProp.call(source, prop) && exclude.indexOf(prop) < 0)
        target[prop] = source[prop];
    if (source != null && __getOwnPropSymbols)
      for (var prop of __getOwnPropSymbols(source)) {
        if (exclude.indexOf(prop) < 0 && __propIsEnum.call(source, prop))
          target[prop] = source[prop];
      }
    return target;
  };
  var __commonJS = (cb, mod) => function __require() {
    return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
    // If the importer is in node compatibility mode or this is not an ESM
    // file that has been converted to a CommonJS file using a Babel-
    // compatible transform (i.e. "__esModule" has not been set), then set
    // "default" to the CommonJS "module.exports" for node compatibility.
    isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
    mod
  ));

  // node_modules/zdog/js/boilerplate.js
  var require_boilerplate = __commonJS({
    "node_modules/zdog/js/boilerplate.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory();
        } else {
          root.Zdog = factory();
        }
      })(exports, function factory() {
        var Zdog2 = {};
        Zdog2.TAU = Math.PI * 2;
        Zdog2.extend = function(a, b) {
          for (var prop in b) {
            a[prop] = b[prop];
          }
          return a;
        };
        Zdog2.lerp = function(a, b, alpha) {
          return (b - a) * alpha + a;
        };
        Zdog2.modulo = function(num, div) {
          return (num % div + div) % div;
        };
        var powerMultipliers = {
          2: function(a) {
            return a * a;
          },
          3: function(a) {
            return a * a * a;
          },
          4: function(a) {
            return a * a * a * a;
          },
          5: function(a) {
            return a * a * a * a * a;
          }
        };
        Zdog2.easeInOut = function(alpha, power) {
          if (power == 1) {
            return alpha;
          }
          alpha = Math.max(0, Math.min(1, alpha));
          var isFirstHalf = alpha < 0.5;
          var slope = isFirstHalf ? alpha : 1 - alpha;
          slope /= 0.5;
          var powerMultiplier = powerMultipliers[power] || powerMultipliers[2];
          var curve = powerMultiplier(slope);
          curve /= 2;
          return isFirstHalf ? curve : 1 - curve;
        };
        return Zdog2;
      });
    }
  });

  // node_modules/zdog/js/canvas-renderer.js
  var require_canvas_renderer = __commonJS({
    "node_modules/zdog/js/canvas-renderer.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory();
        } else {
          root.Zdog.CanvasRenderer = factory();
        }
      })(exports, function factory() {
        var CanvasRenderer = { isCanvas: true };
        CanvasRenderer.begin = function(ctx) {
          ctx.beginPath();
        };
        CanvasRenderer.move = function(ctx, elem, point) {
          ctx.moveTo(point.x, point.y);
        };
        CanvasRenderer.line = function(ctx, elem, point) {
          ctx.lineTo(point.x, point.y);
        };
        CanvasRenderer.bezier = function(ctx, elem, cp0, cp1, end) {
          ctx.bezierCurveTo(cp0.x, cp0.y, cp1.x, cp1.y, end.x, end.y);
        };
        CanvasRenderer.closePath = function(ctx) {
          ctx.closePath();
        };
        CanvasRenderer.setPath = function() {
        };
        CanvasRenderer.renderPath = function(ctx, elem, pathCommands, isClosed) {
          this.begin(ctx, elem);
          pathCommands.forEach(function(command) {
            command.render(ctx, elem, CanvasRenderer);
          });
          if (isClosed) {
            this.closePath(ctx, elem);
          }
        };
        CanvasRenderer.stroke = function(ctx, elem, isStroke, color, lineWidth) {
          if (!isStroke) {
            return;
          }
          ctx.strokeStyle = color;
          ctx.lineWidth = lineWidth;
          ctx.stroke();
        };
        CanvasRenderer.fill = function(ctx, elem, isFill, color) {
          if (!isFill) {
            return;
          }
          ctx.fillStyle = color;
          ctx.fill();
        };
        CanvasRenderer.end = function() {
        };
        return CanvasRenderer;
      });
    }
  });

  // node_modules/zdog/js/svg-renderer.js
  var require_svg_renderer = __commonJS({
    "node_modules/zdog/js/svg-renderer.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory();
        } else {
          root.Zdog.SvgRenderer = factory();
        }
      })(exports, function factory() {
        var SvgRenderer = { isSvg: true };
        var round = SvgRenderer.round = function(num) {
          return Math.round(num * 1e3) / 1e3;
        };
        function getPointString(point) {
          return round(point.x) + "," + round(point.y) + " ";
        }
        SvgRenderer.begin = function() {
        };
        SvgRenderer.move = function(svg, elem, point) {
          return "M" + getPointString(point);
        };
        SvgRenderer.line = function(svg, elem, point) {
          return "L" + getPointString(point);
        };
        SvgRenderer.bezier = function(svg, elem, cp0, cp1, end) {
          return "C" + getPointString(cp0) + getPointString(cp1) + getPointString(end);
        };
        SvgRenderer.closePath = function() {
          return "Z";
        };
        SvgRenderer.setPath = function(svg, elem, pathValue) {
          elem.setAttribute("d", pathValue);
        };
        SvgRenderer.renderPath = function(svg, elem, pathCommands, isClosed) {
          var pathValue = "";
          pathCommands.forEach(function(command) {
            pathValue += command.render(svg, elem, SvgRenderer);
          });
          if (isClosed) {
            pathValue += this.closePath(svg, elem);
          }
          this.setPath(svg, elem, pathValue);
        };
        SvgRenderer.stroke = function(svg, elem, isStroke, color, lineWidth) {
          if (!isStroke) {
            return;
          }
          elem.setAttribute("stroke", color);
          elem.setAttribute("stroke-width", lineWidth);
        };
        SvgRenderer.fill = function(svg, elem, isFill, color) {
          var fillColor = isFill ? color : "none";
          elem.setAttribute("fill", fillColor);
        };
        SvgRenderer.end = function(svg, elem) {
          svg.appendChild(elem);
        };
        return SvgRenderer;
      });
    }
  });

  // node_modules/zdog/js/vector.js
  var require_vector = __commonJS({
    "node_modules/zdog/js/vector.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(require_boilerplate());
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.Vector = factory(Zdog2);
        }
      })(exports, function factory(utils) {
        function Vector(position) {
          this.set(position);
        }
        var TAU = utils.TAU;
        Vector.prototype.set = function(pos) {
          this.x = pos && pos.x || 0;
          this.y = pos && pos.y || 0;
          this.z = pos && pos.z || 0;
          return this;
        };
        Vector.prototype.write = function(pos) {
          if (!pos) {
            return this;
          }
          this.x = pos.x != void 0 ? pos.x : this.x;
          this.y = pos.y != void 0 ? pos.y : this.y;
          this.z = pos.z != void 0 ? pos.z : this.z;
          return this;
        };
        Vector.prototype.rotate = function(rotation) {
          if (!rotation) {
            return;
          }
          this.rotateZ(rotation.z);
          this.rotateY(rotation.y);
          this.rotateX(rotation.x);
          return this;
        };
        Vector.prototype.rotateZ = function(angle) {
          rotateProperty(this, angle, "x", "y");
        };
        Vector.prototype.rotateX = function(angle) {
          rotateProperty(this, angle, "y", "z");
        };
        Vector.prototype.rotateY = function(angle) {
          rotateProperty(this, angle, "x", "z");
        };
        function rotateProperty(vec, angle, propA, propB) {
          if (!angle || angle % TAU === 0) {
            return;
          }
          var cos = Math.cos(angle);
          var sin = Math.sin(angle);
          var a = vec[propA];
          var b = vec[propB];
          vec[propA] = a * cos - b * sin;
          vec[propB] = b * cos + a * sin;
        }
        Vector.prototype.isSame = function(pos) {
          if (!pos) {
            return false;
          }
          return this.x === pos.x && this.y === pos.y && this.z === pos.z;
        };
        Vector.prototype.add = function(pos) {
          if (!pos) {
            return this;
          }
          this.x += pos.x || 0;
          this.y += pos.y || 0;
          this.z += pos.z || 0;
          return this;
        };
        Vector.prototype.subtract = function(pos) {
          if (!pos) {
            return this;
          }
          this.x -= pos.x || 0;
          this.y -= pos.y || 0;
          this.z -= pos.z || 0;
          return this;
        };
        Vector.prototype.multiply = function(pos) {
          if (pos == void 0) {
            return this;
          }
          if (typeof pos == "number") {
            this.x *= pos;
            this.y *= pos;
            this.z *= pos;
          } else {
            this.x *= pos.x != void 0 ? pos.x : 1;
            this.y *= pos.y != void 0 ? pos.y : 1;
            this.z *= pos.z != void 0 ? pos.z : 1;
          }
          return this;
        };
        Vector.prototype.transform = function(translation, rotation, scale) {
          this.multiply(scale);
          this.rotate(rotation);
          this.add(translation);
          return this;
        };
        Vector.prototype.lerp = function(pos, alpha) {
          this.x = utils.lerp(this.x, pos.x || 0, alpha);
          this.y = utils.lerp(this.y, pos.y || 0, alpha);
          this.z = utils.lerp(this.z, pos.z || 0, alpha);
          return this;
        };
        Vector.prototype.magnitude = function() {
          var sum = this.x * this.x + this.y * this.y + this.z * this.z;
          return getMagnitudeSqrt(sum);
        };
        function getMagnitudeSqrt(sum) {
          if (Math.abs(sum - 1) < 1e-8) {
            return 1;
          }
          return Math.sqrt(sum);
        }
        Vector.prototype.magnitude2d = function() {
          var sum = this.x * this.x + this.y * this.y;
          return getMagnitudeSqrt(sum);
        };
        Vector.prototype.copy = function() {
          return new Vector(this);
        };
        return Vector;
      });
    }
  });

  // node_modules/zdog/js/anchor.js
  var require_anchor = __commonJS({
    "node_modules/zdog/js/anchor.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(
            require_boilerplate(),
            require_vector(),
            require_canvas_renderer(),
            require_svg_renderer()
          );
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.Anchor = factory(
            Zdog2,
            Zdog2.Vector,
            Zdog2.CanvasRenderer,
            Zdog2.SvgRenderer
          );
        }
      })(exports, function factory(utils, Vector, CanvasRenderer, SvgRenderer) {
        var TAU = utils.TAU;
        var onePoint = { x: 1, y: 1, z: 1 };
        function Anchor(options) {
          this.create(options || {});
        }
        Anchor.prototype.create = function(options) {
          this.children = [];
          utils.extend(this, this.constructor.defaults);
          this.setOptions(options);
          this.translate = new Vector(options.translate);
          this.rotate = new Vector(options.rotate);
          this.scale = new Vector(onePoint).multiply(this.scale);
          this.origin = new Vector();
          this.renderOrigin = new Vector();
          if (this.addTo) {
            this.addTo.addChild(this);
          }
        };
        Anchor.defaults = {};
        Anchor.optionKeys = Object.keys(Anchor.defaults).concat([
          "rotate",
          "translate",
          "scale",
          "addTo"
        ]);
        Anchor.prototype.setOptions = function(options) {
          var optionKeys = this.constructor.optionKeys;
          for (var key in options) {
            if (optionKeys.indexOf(key) != -1) {
              this[key] = options[key];
            }
          }
        };
        Anchor.prototype.addChild = function(shape) {
          if (this.children.indexOf(shape) != -1) {
            return;
          }
          shape.remove();
          shape.addTo = this;
          this.children.push(shape);
        };
        Anchor.prototype.removeChild = function(shape) {
          var index = this.children.indexOf(shape);
          if (index != -1) {
            this.children.splice(index, 1);
          }
        };
        Anchor.prototype.remove = function() {
          if (this.addTo) {
            this.addTo.removeChild(this);
          }
        };
        Anchor.prototype.update = function() {
          this.reset();
          this.children.forEach(function(child) {
            child.update();
          });
          this.transform(this.translate, this.rotate, this.scale);
        };
        Anchor.prototype.reset = function() {
          this.renderOrigin.set(this.origin);
        };
        Anchor.prototype.transform = function(translation, rotation, scale) {
          this.renderOrigin.transform(translation, rotation, scale);
          this.children.forEach(function(child) {
            child.transform(translation, rotation, scale);
          });
        };
        Anchor.prototype.updateGraph = function() {
          this.update();
          this.updateFlatGraph();
          this.flatGraph.forEach(function(item) {
            item.updateSortValue();
          });
          this.flatGraph.sort(Anchor.shapeSorter);
        };
        Anchor.shapeSorter = function(a, b) {
          return a.sortValue - b.sortValue;
        };
        Object.defineProperty(Anchor.prototype, "flatGraph", {
          get: function() {
            if (!this._flatGraph) {
              this.updateFlatGraph();
            }
            return this._flatGraph;
          },
          set: function(graph) {
            this._flatGraph = graph;
          }
        });
        Anchor.prototype.updateFlatGraph = function() {
          this.flatGraph = this.getFlatGraph();
        };
        Anchor.prototype.getFlatGraph = function() {
          var flatGraph = [this];
          return this.addChildFlatGraph(flatGraph);
        };
        Anchor.prototype.addChildFlatGraph = function(flatGraph) {
          this.children.forEach(function(child) {
            var childFlatGraph = child.getFlatGraph();
            Array.prototype.push.apply(flatGraph, childFlatGraph);
          });
          return flatGraph;
        };
        Anchor.prototype.updateSortValue = function() {
          this.sortValue = this.renderOrigin.z;
        };
        Anchor.prototype.render = function() {
        };
        Anchor.prototype.renderGraphCanvas = function(ctx) {
          if (!ctx) {
            throw new Error("ctx is " + ctx + ". Canvas context required for render. Check .renderGraphCanvas( ctx ).");
          }
          this.flatGraph.forEach(function(item) {
            item.render(ctx, CanvasRenderer);
          });
        };
        Anchor.prototype.renderGraphSvg = function(svg) {
          if (!svg) {
            throw new Error("svg is " + svg + ". SVG required for render. Check .renderGraphSvg( svg ).");
          }
          this.flatGraph.forEach(function(item) {
            item.render(svg, SvgRenderer);
          });
        };
        Anchor.prototype.copy = function(options) {
          var itemOptions = {};
          var optionKeys = this.constructor.optionKeys;
          optionKeys.forEach(function(key) {
            itemOptions[key] = this[key];
          }, this);
          utils.extend(itemOptions, options);
          var ItemClass = this.constructor;
          return new ItemClass(itemOptions);
        };
        Anchor.prototype.copyGraph = function(options) {
          var clone = this.copy(options);
          this.children.forEach(function(child) {
            child.copyGraph({
              addTo: clone
            });
          });
          return clone;
        };
        Anchor.prototype.normalizeRotate = function() {
          this.rotate.x = utils.modulo(this.rotate.x, TAU);
          this.rotate.y = utils.modulo(this.rotate.y, TAU);
          this.rotate.z = utils.modulo(this.rotate.z, TAU);
        };
        function getSubclass(Super) {
          return function(defaults) {
            function Item(options) {
              this.create(options || {});
            }
            Item.prototype = Object.create(Super.prototype);
            Item.prototype.constructor = Item;
            Item.defaults = utils.extend({}, Super.defaults);
            utils.extend(Item.defaults, defaults);
            Item.optionKeys = Super.optionKeys.slice(0);
            Object.keys(Item.defaults).forEach(function(key) {
              if (!Item.optionKeys.indexOf(key) != 1) {
                Item.optionKeys.push(key);
              }
            });
            Item.subclass = getSubclass(Item);
            return Item;
          };
        }
        Anchor.subclass = getSubclass(Anchor);
        return Anchor;
      });
    }
  });

  // node_modules/zdog/js/dragger.js
  var require_dragger = __commonJS({
    "node_modules/zdog/js/dragger.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory();
        } else {
          root.Zdog.Dragger = factory();
        }
      })(exports, function factory() {
        var hasWindow = typeof window != "undefined";
        var downEvent = "mousedown";
        var moveEvent = "mousemove";
        var upEvent = "mouseup";
        if (hasWindow) {
          if (window.PointerEvent) {
            downEvent = "pointerdown";
            moveEvent = "pointermove";
            upEvent = "pointerup";
          } else if ("ontouchstart" in window) {
            downEvent = "touchstart";
            moveEvent = "touchmove";
            upEvent = "touchend";
          }
        }
        function noop() {
        }
        function Dragger(options) {
          this.create(options || {});
        }
        Dragger.prototype.create = function(options) {
          this.onDragStart = options.onDragStart || noop;
          this.onDragMove = options.onDragMove || noop;
          this.onDragEnd = options.onDragEnd || noop;
          this.bindDrag(options.startElement);
        };
        Dragger.prototype.bindDrag = function(element) {
          element = this.getQueryElement(element);
          if (!element) {
            return;
          }
          element.style.touchAction = "none";
          element.addEventListener(downEvent, this);
        };
        Dragger.prototype.getQueryElement = function(element) {
          if (typeof element == "string") {
            element = document.querySelector(element);
          }
          return element;
        };
        Dragger.prototype.handleEvent = function(event) {
          var method = this["on" + event.type];
          if (method) {
            method.call(this, event);
          }
        };
        Dragger.prototype.onmousedown = Dragger.prototype.onpointerdown = function(event) {
          this.dragStart(event, event);
        };
        Dragger.prototype.ontouchstart = function(event) {
          this.dragStart(event, event.changedTouches[0]);
        };
        Dragger.prototype.dragStart = function(event, pointer) {
          event.preventDefault();
          this.dragStartX = pointer.pageX;
          this.dragStartY = pointer.pageY;
          if (hasWindow) {
            window.addEventListener(moveEvent, this);
            window.addEventListener(upEvent, this);
          }
          this.onDragStart(pointer);
        };
        Dragger.prototype.ontouchmove = function(event) {
          this.dragMove(event, event.changedTouches[0]);
        };
        Dragger.prototype.onmousemove = Dragger.prototype.onpointermove = function(event) {
          this.dragMove(event, event);
        };
        Dragger.prototype.dragMove = function(event, pointer) {
          event.preventDefault();
          var moveX = pointer.pageX - this.dragStartX;
          var moveY = pointer.pageY - this.dragStartY;
          this.onDragMove(pointer, moveX, moveY);
        };
        Dragger.prototype.onmouseup = Dragger.prototype.onpointerup = Dragger.prototype.ontouchend = Dragger.prototype.dragEnd = function() {
          window.removeEventListener(moveEvent, this);
          window.removeEventListener(upEvent, this);
          this.onDragEnd();
        };
        return Dragger;
      });
    }
  });

  // node_modules/zdog/js/illustration.js
  var require_illustration = __commonJS({
    "node_modules/zdog/js/illustration.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(
            require_boilerplate(),
            require_anchor(),
            require_dragger()
          );
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.Illustration = factory(Zdog2, Zdog2.Anchor, Zdog2.Dragger);
        }
      })(exports, function factory(utils, Anchor, Dragger) {
        function noop() {
        }
        var TAU = utils.TAU;
        var Illustration = Anchor.subclass({
          element: void 0,
          centered: true,
          zoom: 1,
          dragRotate: false,
          resize: false,
          onPrerender: noop,
          onDragStart: noop,
          onDragMove: noop,
          onDragEnd: noop,
          onResize: noop
        });
        utils.extend(Illustration.prototype, Dragger.prototype);
        Illustration.prototype.create = function(options) {
          Anchor.prototype.create.call(this, options);
          Dragger.prototype.create.call(this, options);
          this.setElement(this.element);
          this.setDragRotate(this.dragRotate);
          this.setResize(this.resize);
        };
        Illustration.prototype.setElement = function(element) {
          element = this.getQueryElement(element);
          if (!element) {
            throw new Error("Zdog.Illustration element required. Set to " + element);
          }
          var nodeName = element.nodeName.toLowerCase();
          if (nodeName == "canvas") {
            this.setCanvas(element);
          } else if (nodeName == "svg") {
            this.setSvg(element);
          }
        };
        Illustration.prototype.setSize = function(width, height) {
          width = Math.round(width);
          height = Math.round(height);
          if (this.isCanvas) {
            this.setSizeCanvas(width, height);
          } else if (this.isSvg) {
            this.setSizeSvg(width, height);
          }
        };
        Illustration.prototype.setResize = function(resize) {
          this.resize = resize;
          if (!this.resizeListener) {
            this.resizeListener = this.onWindowResize.bind(this);
          }
          if (resize) {
            window.addEventListener("resize", this.resizeListener);
            this.onWindowResize();
          } else {
            window.removeEventListener("resize", this.resizeListener);
          }
        };
        Illustration.prototype.onWindowResize = function() {
          this.setMeasuredSize();
          this.onResize(this.width, this.height);
        };
        Illustration.prototype.setMeasuredSize = function() {
          var width, height;
          var isFullscreen = this.resize == "fullscreen";
          if (isFullscreen) {
            width = window.innerWidth;
            height = window.innerHeight;
          } else {
            var rect = this.element.getBoundingClientRect();
            width = rect.width;
            height = rect.height;
          }
          this.setSize(width, height);
        };
        Illustration.prototype.renderGraph = function(item) {
          if (this.isCanvas) {
            this.renderGraphCanvas(item);
          } else if (this.isSvg) {
            this.renderGraphSvg(item);
          }
        };
        Illustration.prototype.updateRenderGraph = function(item) {
          this.updateGraph();
          this.renderGraph(item);
        };
        Illustration.prototype.setCanvas = function(element) {
          this.element = element;
          this.isCanvas = true;
          this.ctx = this.element.getContext("2d");
          this.setSizeCanvas(element.width, element.height);
        };
        Illustration.prototype.setSizeCanvas = function(width, height) {
          this.width = width;
          this.height = height;
          var pixelRatio = this.pixelRatio = window.devicePixelRatio || 1;
          this.element.width = this.canvasWidth = width * pixelRatio;
          this.element.height = this.canvasHeight = height * pixelRatio;
          var needsHighPixelRatioSizing = pixelRatio > 1 && !this.resize;
          if (needsHighPixelRatioSizing) {
            this.element.style.width = width + "px";
            this.element.style.height = height + "px";
          }
        };
        Illustration.prototype.renderGraphCanvas = function(item) {
          item = item || this;
          this.prerenderCanvas();
          Anchor.prototype.renderGraphCanvas.call(item, this.ctx);
          this.postrenderCanvas();
        };
        Illustration.prototype.prerenderCanvas = function() {
          var ctx = this.ctx;
          ctx.lineCap = "round";
          ctx.lineJoin = "round";
          ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
          ctx.save();
          if (this.centered) {
            var centerX = this.width / 2 * this.pixelRatio;
            var centerY = this.height / 2 * this.pixelRatio;
            ctx.translate(centerX, centerY);
          }
          var scale = this.pixelRatio * this.zoom;
          ctx.scale(scale, scale);
          this.onPrerender(ctx);
        };
        Illustration.prototype.postrenderCanvas = function() {
          this.ctx.restore();
        };
        Illustration.prototype.setSvg = function(element) {
          this.element = element;
          this.isSvg = true;
          this.pixelRatio = 1;
          var width = element.getAttribute("width");
          var height = element.getAttribute("height");
          this.setSizeSvg(width, height);
        };
        Illustration.prototype.setSizeSvg = function(width, height) {
          this.width = width;
          this.height = height;
          var viewWidth = width / this.zoom;
          var viewHeight = height / this.zoom;
          var viewX = this.centered ? -viewWidth / 2 : 0;
          var viewY = this.centered ? -viewHeight / 2 : 0;
          this.element.setAttribute("viewBox", viewX + " " + viewY + " " + viewWidth + " " + viewHeight);
          if (this.resize) {
            this.element.removeAttribute("width");
            this.element.removeAttribute("height");
          } else {
            this.element.setAttribute("width", width);
            this.element.setAttribute("height", height);
          }
        };
        Illustration.prototype.renderGraphSvg = function(item) {
          item = item || this;
          empty(this.element);
          this.onPrerender(this.element);
          Anchor.prototype.renderGraphSvg.call(item, this.element);
        };
        function empty(element) {
          while (element.firstChild) {
            element.removeChild(element.firstChild);
          }
        }
        Illustration.prototype.setDragRotate = function(item) {
          if (!item) {
            return;
          } else if (item === true) {
            item = this;
          }
          this.dragRotate = item;
          this.bindDrag(this.element);
        };
        Illustration.prototype.dragStart = function() {
          this.dragStartRX = this.dragRotate.rotate.x;
          this.dragStartRY = this.dragRotate.rotate.y;
          Dragger.prototype.dragStart.apply(this, arguments);
        };
        Illustration.prototype.dragMove = function(event, pointer) {
          var moveX = pointer.pageX - this.dragStartX;
          var moveY = pointer.pageY - this.dragStartY;
          var displaySize = Math.min(this.width, this.height);
          var moveRY = moveX / displaySize * TAU;
          var moveRX = moveY / displaySize * TAU;
          this.dragRotate.rotate.x = this.dragStartRX - moveRX;
          this.dragRotate.rotate.y = this.dragStartRY - moveRY;
          Dragger.prototype.dragMove.apply(this, arguments);
        };
        return Illustration;
      });
    }
  });

  // node_modules/zdog/js/path-command.js
  var require_path_command = __commonJS({
    "node_modules/zdog/js/path-command.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(require_vector());
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.PathCommand = factory(Zdog2.Vector);
        }
      })(exports, function factory(Vector) {
        function PathCommand(method, points, previousPoint) {
          this.method = method;
          this.points = points.map(mapVectorPoint);
          this.renderPoints = points.map(mapNewVector);
          this.previousPoint = previousPoint;
          this.endRenderPoint = this.renderPoints[this.renderPoints.length - 1];
          if (method == "arc") {
            this.controlPoints = [new Vector(), new Vector()];
          }
        }
        function mapVectorPoint(point) {
          if (point instanceof Vector) {
            return point;
          } else {
            return new Vector(point);
          }
        }
        function mapNewVector(point) {
          return new Vector(point);
        }
        PathCommand.prototype.reset = function() {
          var points = this.points;
          this.renderPoints.forEach(function(renderPoint, i) {
            var point = points[i];
            renderPoint.set(point);
          });
        };
        PathCommand.prototype.transform = function(translation, rotation, scale) {
          this.renderPoints.forEach(function(renderPoint) {
            renderPoint.transform(translation, rotation, scale);
          });
        };
        PathCommand.prototype.render = function(ctx, elem, renderer) {
          return this[this.method](ctx, elem, renderer);
        };
        PathCommand.prototype.move = function(ctx, elem, renderer) {
          return renderer.move(ctx, elem, this.renderPoints[0]);
        };
        PathCommand.prototype.line = function(ctx, elem, renderer) {
          return renderer.line(ctx, elem, this.renderPoints[0]);
        };
        PathCommand.prototype.bezier = function(ctx, elem, renderer) {
          var cp0 = this.renderPoints[0];
          var cp1 = this.renderPoints[1];
          var end = this.renderPoints[2];
          return renderer.bezier(ctx, elem, cp0, cp1, end);
        };
        var arcHandleLength = 9 / 16;
        PathCommand.prototype.arc = function(ctx, elem, renderer) {
          var prev = this.previousPoint;
          var corner = this.renderPoints[0];
          var end = this.renderPoints[1];
          var cp0 = this.controlPoints[0];
          var cp1 = this.controlPoints[1];
          cp0.set(prev).lerp(corner, arcHandleLength);
          cp1.set(end).lerp(corner, arcHandleLength);
          return renderer.bezier(ctx, elem, cp0, cp1, end);
        };
        return PathCommand;
      });
    }
  });

  // node_modules/zdog/js/shape.js
  var require_shape = __commonJS({
    "node_modules/zdog/js/shape.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(
            require_boilerplate(),
            require_vector(),
            require_path_command(),
            require_anchor()
          );
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.Shape = factory(Zdog2, Zdog2.Vector, Zdog2.PathCommand, Zdog2.Anchor);
        }
      })(exports, function factory(utils, Vector, PathCommand, Anchor) {
        var Shape = Anchor.subclass({
          stroke: 1,
          fill: false,
          color: "#333",
          closed: true,
          visible: true,
          path: [{}],
          front: { z: 1 },
          backface: true
        });
        Shape.prototype.create = function(options) {
          Anchor.prototype.create.call(this, options);
          this.updatePath();
          this.front = new Vector(options.front || this.front);
          this.renderFront = new Vector(this.front);
          this.renderNormal = new Vector();
        };
        var actionNames = [
          "move",
          "line",
          "bezier",
          "arc"
        ];
        Shape.prototype.updatePath = function() {
          this.setPath();
          this.updatePathCommands();
        };
        Shape.prototype.setPath = function() {
        };
        Shape.prototype.updatePathCommands = function() {
          var previousPoint;
          this.pathCommands = this.path.map(function(pathPart, i) {
            var keys = Object.keys(pathPart);
            var method = keys[0];
            var points = pathPart[method];
            var isInstruction = keys.length == 1 && actionNames.indexOf(method) != -1;
            if (!isInstruction) {
              method = "line";
              points = pathPart;
            }
            var isLineOrMove = method == "line" || method == "move";
            var isPointsArray = Array.isArray(points);
            if (isLineOrMove && !isPointsArray) {
              points = [points];
            }
            method = i === 0 ? "move" : method;
            var command = new PathCommand(method, points, previousPoint);
            previousPoint = command.endRenderPoint;
            return command;
          });
        };
        Shape.prototype.reset = function() {
          this.renderOrigin.set(this.origin);
          this.renderFront.set(this.front);
          this.pathCommands.forEach(function(command) {
            command.reset();
          });
        };
        Shape.prototype.transform = function(translation, rotation, scale) {
          this.renderOrigin.transform(translation, rotation, scale);
          this.renderFront.transform(translation, rotation, scale);
          this.renderNormal.set(this.renderOrigin).subtract(this.renderFront);
          this.pathCommands.forEach(function(command) {
            command.transform(translation, rotation, scale);
          });
          this.children.forEach(function(child) {
            child.transform(translation, rotation, scale);
          });
        };
        Shape.prototype.updateSortValue = function() {
          var pointCount = this.pathCommands.length;
          var firstPoint = this.pathCommands[0].endRenderPoint;
          var lastPoint = this.pathCommands[pointCount - 1].endRenderPoint;
          var isSelfClosing = pointCount > 2 && firstPoint.isSame(lastPoint);
          if (isSelfClosing) {
            pointCount -= 1;
          }
          var sortValueTotal = 0;
          for (var i = 0; i < pointCount; i++) {
            sortValueTotal += this.pathCommands[i].endRenderPoint.z;
          }
          this.sortValue = sortValueTotal / pointCount;
        };
        Shape.prototype.render = function(ctx, renderer) {
          var length = this.pathCommands.length;
          if (!this.visible || !length) {
            return;
          }
          this.isFacingBack = this.renderNormal.z > 0;
          if (!this.backface && this.isFacingBack) {
            return;
          }
          if (!renderer) {
            throw new Error("Zdog renderer required. Set to " + renderer);
          }
          var isDot = length == 1;
          if (renderer.isCanvas && isDot) {
            this.renderCanvasDot(ctx, renderer);
          } else {
            this.renderPath(ctx, renderer);
          }
        };
        var TAU = utils.TAU;
        Shape.prototype.renderCanvasDot = function(ctx) {
          var lineWidth = this.getLineWidth();
          if (!lineWidth) {
            return;
          }
          ctx.fillStyle = this.getRenderColor();
          var point = this.pathCommands[0].endRenderPoint;
          ctx.beginPath();
          var radius = lineWidth / 2;
          ctx.arc(point.x, point.y, radius, 0, TAU);
          ctx.fill();
        };
        Shape.prototype.getLineWidth = function() {
          if (!this.stroke) {
            return 0;
          }
          if (this.stroke == true) {
            return 1;
          }
          return this.stroke;
        };
        Shape.prototype.getRenderColor = function() {
          var isBackfaceColor = typeof this.backface == "string" && this.isFacingBack;
          var color = isBackfaceColor ? this.backface : this.color;
          return color;
        };
        Shape.prototype.renderPath = function(ctx, renderer) {
          var elem = this.getRenderElement(ctx, renderer);
          var isTwoPoints = this.pathCommands.length == 2 && this.pathCommands[1].method == "line";
          var isClosed = !isTwoPoints && this.closed;
          var color = this.getRenderColor();
          renderer.renderPath(ctx, elem, this.pathCommands, isClosed);
          renderer.stroke(ctx, elem, this.stroke, color, this.getLineWidth());
          renderer.fill(ctx, elem, this.fill, color);
          renderer.end(ctx, elem);
        };
        var svgURI = "http://www.w3.org/2000/svg";
        Shape.prototype.getRenderElement = function(ctx, renderer) {
          if (!renderer.isSvg) {
            return;
          }
          if (!this.svgElement) {
            this.svgElement = document.createElementNS(svgURI, "path");
            this.svgElement.setAttribute("stroke-linecap", "round");
            this.svgElement.setAttribute("stroke-linejoin", "round");
          }
          return this.svgElement;
        };
        return Shape;
      });
    }
  });

  // node_modules/zdog/js/group.js
  var require_group = __commonJS({
    "node_modules/zdog/js/group.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(require_anchor());
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.Group = factory(Zdog2.Anchor);
        }
      })(exports, function factory(Anchor) {
        var Group = Anchor.subclass({
          updateSort: false,
          visible: true
        });
        Group.prototype.updateSortValue = function() {
          var sortValueTotal = 0;
          this.flatGraph.forEach(function(item) {
            item.updateSortValue();
            sortValueTotal += item.sortValue;
          });
          this.sortValue = sortValueTotal / this.flatGraph.length;
          if (this.updateSort) {
            this.flatGraph.sort(Anchor.shapeSorter);
          }
        };
        Group.prototype.render = function(ctx, renderer) {
          if (!this.visible) {
            return;
          }
          this.flatGraph.forEach(function(item) {
            item.render(ctx, renderer);
          });
        };
        Group.prototype.updateFlatGraph = function() {
          var flatGraph = [];
          this.flatGraph = this.addChildFlatGraph(flatGraph);
        };
        Group.prototype.getFlatGraph = function() {
          return [this];
        };
        return Group;
      });
    }
  });

  // node_modules/zdog/js/rect.js
  var require_rect = __commonJS({
    "node_modules/zdog/js/rect.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(require_shape());
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.Rect = factory(Zdog2.Shape);
        }
      })(exports, function factory(Shape) {
        var Rect = Shape.subclass({
          width: 1,
          height: 1
        });
        Rect.prototype.setPath = function() {
          var x = this.width / 2;
          var y = this.height / 2;
          this.path = [
            { x: -x, y: -y },
            { x, y: -y },
            { x, y },
            { x: -x, y }
          ];
        };
        return Rect;
      });
    }
  });

  // node_modules/zdog/js/rounded-rect.js
  var require_rounded_rect = __commonJS({
    "node_modules/zdog/js/rounded-rect.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(require_shape());
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.RoundedRect = factory(Zdog2.Shape);
        }
      })(exports, function factory(Shape) {
        var RoundedRect = Shape.subclass({
          width: 1,
          height: 1,
          cornerRadius: 0.25,
          closed: false
        });
        RoundedRect.prototype.setPath = function() {
          var xA = this.width / 2;
          var yA = this.height / 2;
          var shortSide = Math.min(xA, yA);
          var cornerRadius = Math.min(this.cornerRadius, shortSide);
          var xB = xA - cornerRadius;
          var yB = yA - cornerRadius;
          var path = [
            // top right corner
            { x: xB, y: -yA },
            { arc: [
              { x: xA, y: -yA },
              { x: xA, y: -yB }
            ] }
          ];
          if (yB) {
            path.push({ x: xA, y: yB });
          }
          path.push({ arc: [
            { x: xA, y: yA },
            { x: xB, y: yA }
          ] });
          if (xB) {
            path.push({ x: -xB, y: yA });
          }
          path.push({ arc: [
            { x: -xA, y: yA },
            { x: -xA, y: yB }
          ] });
          if (yB) {
            path.push({ x: -xA, y: -yB });
          }
          path.push({ arc: [
            { x: -xA, y: -yA },
            { x: -xB, y: -yA }
          ] });
          if (xB) {
            path.push({ x: xB, y: -yA });
          }
          this.path = path;
        };
        return RoundedRect;
      });
    }
  });

  // node_modules/zdog/js/ellipse.js
  var require_ellipse = __commonJS({
    "node_modules/zdog/js/ellipse.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(require_shape());
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.Ellipse = factory(Zdog2.Shape);
        }
      })(exports, function factory(Shape) {
        var Ellipse = Shape.subclass({
          diameter: 1,
          width: void 0,
          height: void 0,
          quarters: 4,
          closed: false
        });
        Ellipse.prototype.setPath = function() {
          var width = this.width != void 0 ? this.width : this.diameter;
          var height = this.height != void 0 ? this.height : this.diameter;
          var x = width / 2;
          var y = height / 2;
          this.path = [
            { x: 0, y: -y },
            { arc: [
              // top right
              { x, y: -y },
              { x, y: 0 }
            ] }
          ];
          if (this.quarters > 1) {
            this.path.push({ arc: [
              { x, y },
              { x: 0, y }
            ] });
          }
          if (this.quarters > 2) {
            this.path.push({ arc: [
              { x: -x, y },
              { x: -x, y: 0 }
            ] });
          }
          if (this.quarters > 3) {
            this.path.push({ arc: [
              { x: -x, y: -y },
              { x: 0, y: -y }
            ] });
          }
        };
        return Ellipse;
      });
    }
  });

  // node_modules/zdog/js/polygon.js
  var require_polygon = __commonJS({
    "node_modules/zdog/js/polygon.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(require_boilerplate(), require_shape());
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.Polygon = factory(Zdog2, Zdog2.Shape);
        }
      })(exports, function factory(utils, Shape) {
        var Polygon = Shape.subclass({
          sides: 3,
          radius: 0.5
        });
        var TAU = utils.TAU;
        Polygon.prototype.setPath = function() {
          this.path = [];
          for (var i = 0; i < this.sides; i++) {
            var theta = i / this.sides * TAU - TAU / 4;
            var x = Math.cos(theta) * this.radius;
            var y = Math.sin(theta) * this.radius;
            this.path.push({ x, y });
          }
        };
        return Polygon;
      });
    }
  });

  // node_modules/zdog/js/hemisphere.js
  var require_hemisphere = __commonJS({
    "node_modules/zdog/js/hemisphere.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(
            require_boilerplate(),
            require_vector(),
            require_anchor(),
            require_ellipse()
          );
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.Hemisphere = factory(Zdog2, Zdog2.Vector, Zdog2.Anchor, Zdog2.Ellipse);
        }
      })(exports, function factory(utils, Vector, Anchor, Ellipse) {
        var Hemisphere = Ellipse.subclass({
          fill: true
        });
        var TAU = utils.TAU;
        Hemisphere.prototype.create = function() {
          Ellipse.prototype.create.apply(this, arguments);
          this.apex = new Anchor({
            addTo: this,
            translate: { z: this.diameter / 2 }
          });
          this.renderCentroid = new Vector();
        };
        Hemisphere.prototype.updateSortValue = function() {
          this.renderCentroid.set(this.renderOrigin).lerp(this.apex.renderOrigin, 3 / 8);
          this.sortValue = this.renderCentroid.z;
        };
        Hemisphere.prototype.render = function(ctx, renderer) {
          this.renderDome(ctx, renderer);
          Ellipse.prototype.render.apply(this, arguments);
        };
        Hemisphere.prototype.renderDome = function(ctx, renderer) {
          if (!this.visible) {
            return;
          }
          var elem = this.getDomeRenderElement(ctx, renderer);
          var contourAngle = Math.atan2(this.renderNormal.y, this.renderNormal.x);
          var domeRadius = this.diameter / 2 * this.renderNormal.magnitude();
          var x = this.renderOrigin.x;
          var y = this.renderOrigin.y;
          if (renderer.isCanvas) {
            var startAngle = contourAngle + TAU / 4;
            var endAngle = contourAngle - TAU / 4;
            ctx.beginPath();
            ctx.arc(x, y, domeRadius, startAngle, endAngle);
          } else if (renderer.isSvg) {
            contourAngle = (contourAngle - TAU / 4) / TAU * 360;
            this.domeSvgElement.setAttribute("d", "M " + -domeRadius + ",0 A " + domeRadius + "," + domeRadius + " 0 0 1 " + domeRadius + ",0");
            this.domeSvgElement.setAttribute(
              "transform",
              "translate(" + x + "," + y + " ) rotate(" + contourAngle + ")"
            );
          }
          renderer.stroke(ctx, elem, this.stroke, this.color, this.getLineWidth());
          renderer.fill(ctx, elem, this.fill, this.color);
          renderer.end(ctx, elem);
        };
        var svgURI = "http://www.w3.org/2000/svg";
        Hemisphere.prototype.getDomeRenderElement = function(ctx, renderer) {
          if (!renderer.isSvg) {
            return;
          }
          if (!this.domeSvgElement) {
            this.domeSvgElement = document.createElementNS(svgURI, "path");
            this.domeSvgElement.setAttribute("stroke-linecap", "round");
            this.domeSvgElement.setAttribute("stroke-linejoin", "round");
          }
          return this.domeSvgElement;
        };
        return Hemisphere;
      });
    }
  });

  // node_modules/zdog/js/cylinder.js
  var require_cylinder = __commonJS({
    "node_modules/zdog/js/cylinder.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(
            require_boilerplate(),
            require_path_command(),
            require_shape(),
            require_group(),
            require_ellipse()
          );
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.Cylinder = factory(
            Zdog2,
            Zdog2.PathCommand,
            Zdog2.Shape,
            Zdog2.Group,
            Zdog2.Ellipse
          );
        }
      })(exports, function factory(utils, PathCommand, Shape, Group, Ellipse) {
        function noop() {
        }
        var CylinderGroup = Group.subclass({
          color: "#333",
          updateSort: true
        });
        CylinderGroup.prototype.create = function() {
          Group.prototype.create.apply(this, arguments);
          this.pathCommands = [
            new PathCommand("move", [{}]),
            new PathCommand("line", [{}])
          ];
        };
        CylinderGroup.prototype.render = function(ctx, renderer) {
          this.renderCylinderSurface(ctx, renderer);
          Group.prototype.render.apply(this, arguments);
        };
        CylinderGroup.prototype.renderCylinderSurface = function(ctx, renderer) {
          if (!this.visible) {
            return;
          }
          var elem = this.getRenderElement(ctx, renderer);
          var frontBase = this.frontBase;
          var rearBase = this.rearBase;
          var scale = frontBase.renderNormal.magnitude();
          var strokeWidth = frontBase.diameter * scale + frontBase.getLineWidth();
          this.pathCommands[0].renderPoints[0].set(frontBase.renderOrigin);
          this.pathCommands[1].renderPoints[0].set(rearBase.renderOrigin);
          if (renderer.isCanvas) {
            ctx.lineCap = "butt";
          }
          renderer.renderPath(ctx, elem, this.pathCommands);
          renderer.stroke(ctx, elem, true, this.color, strokeWidth);
          renderer.end(ctx, elem);
          if (renderer.isCanvas) {
            ctx.lineCap = "round";
          }
        };
        var svgURI = "http://www.w3.org/2000/svg";
        CylinderGroup.prototype.getRenderElement = function(ctx, renderer) {
          if (!renderer.isSvg) {
            return;
          }
          if (!this.svgElement) {
            this.svgElement = document.createElementNS(svgURI, "path");
          }
          return this.svgElement;
        };
        CylinderGroup.prototype.copyGraph = noop;
        var CylinderEllipse = Ellipse.subclass();
        CylinderEllipse.prototype.copyGraph = noop;
        var Cylinder = Shape.subclass({
          diameter: 1,
          length: 1,
          frontFace: void 0,
          fill: true
        });
        var TAU = utils.TAU;
        Cylinder.prototype.create = function() {
          Shape.prototype.create.apply(this, arguments);
          this.group = new CylinderGroup({
            addTo: this,
            color: this.color,
            visible: this.visible
          });
          var baseZ = this.length / 2;
          var baseColor = this.backface || true;
          this.frontBase = this.group.frontBase = new Ellipse({
            addTo: this.group,
            diameter: this.diameter,
            translate: { z: baseZ },
            rotate: { y: TAU / 2 },
            color: this.color,
            stroke: this.stroke,
            fill: this.fill,
            backface: this.frontFace || baseColor,
            visible: this.visible
          });
          this.rearBase = this.group.rearBase = this.frontBase.copy({
            translate: { z: -baseZ },
            rotate: { y: 0 },
            backface: baseColor
          });
        };
        Cylinder.prototype.render = function() {
        };
        var childProperties = ["stroke", "fill", "color", "visible"];
        childProperties.forEach(function(property) {
          var _prop = "_" + property;
          Object.defineProperty(Cylinder.prototype, property, {
            get: function() {
              return this[_prop];
            },
            set: function(value) {
              this[_prop] = value;
              if (this.frontBase) {
                this.frontBase[property] = value;
                this.rearBase[property] = value;
                this.group[property] = value;
              }
            }
          });
        });
        return Cylinder;
      });
    }
  });

  // node_modules/zdog/js/cone.js
  var require_cone = __commonJS({
    "node_modules/zdog/js/cone.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(
            require_boilerplate(),
            require_vector(),
            require_path_command(),
            require_anchor(),
            require_ellipse()
          );
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.Cone = factory(
            Zdog2,
            Zdog2.Vector,
            Zdog2.PathCommand,
            Zdog2.Anchor,
            Zdog2.Ellipse
          );
        }
      })(exports, function factory(utils, Vector, PathCommand, Anchor, Ellipse) {
        var Cone = Ellipse.subclass({
          length: 1,
          fill: true
        });
        var TAU = utils.TAU;
        Cone.prototype.create = function() {
          Ellipse.prototype.create.apply(this, arguments);
          this.apex = new Anchor({
            addTo: this,
            translate: { z: this.length }
          });
          this.renderApex = new Vector();
          this.renderCentroid = new Vector();
          this.tangentA = new Vector();
          this.tangentB = new Vector();
          this.surfacePathCommands = [
            new PathCommand("move", [{}]),
            // points set in renderConeSurface
            new PathCommand("line", [{}]),
            new PathCommand("line", [{}])
          ];
        };
        Cone.prototype.updateSortValue = function() {
          this.renderCentroid.set(this.renderOrigin).lerp(this.apex.renderOrigin, 1 / 3);
          this.sortValue = this.renderCentroid.z;
        };
        Cone.prototype.render = function(ctx, renderer) {
          this.renderConeSurface(ctx, renderer);
          Ellipse.prototype.render.apply(this, arguments);
        };
        Cone.prototype.renderConeSurface = function(ctx, renderer) {
          if (!this.visible) {
            return;
          }
          this.renderApex.set(this.apex.renderOrigin).subtract(this.renderOrigin);
          var scale = this.renderNormal.magnitude();
          var apexDistance = this.renderApex.magnitude2d();
          var normalDistance = this.renderNormal.magnitude2d();
          var eccenAngle = Math.acos(normalDistance / scale);
          var eccen = Math.sin(eccenAngle);
          var radius = this.diameter / 2 * scale;
          var isApexVisible = radius * eccen < apexDistance;
          if (!isApexVisible) {
            return;
          }
          var apexAngle = Math.atan2(this.renderNormal.y, this.renderNormal.x) + TAU / 2;
          var projectLength = apexDistance / eccen;
          var projectAngle = Math.acos(radius / projectLength);
          var tangentA = this.tangentA;
          var tangentB = this.tangentB;
          tangentA.x = Math.cos(projectAngle) * radius * eccen;
          tangentA.y = Math.sin(projectAngle) * radius;
          tangentB.set(this.tangentA);
          tangentB.y *= -1;
          tangentA.rotateZ(apexAngle);
          tangentB.rotateZ(apexAngle);
          tangentA.add(this.renderOrigin);
          tangentB.add(this.renderOrigin);
          this.setSurfaceRenderPoint(0, tangentA);
          this.setSurfaceRenderPoint(1, this.apex.renderOrigin);
          this.setSurfaceRenderPoint(2, tangentB);
          var elem = this.getSurfaceRenderElement(ctx, renderer);
          renderer.renderPath(ctx, elem, this.surfacePathCommands);
          renderer.stroke(ctx, elem, this.stroke, this.color, this.getLineWidth());
          renderer.fill(ctx, elem, this.fill, this.color);
          renderer.end(ctx, elem);
        };
        var svgURI = "http://www.w3.org/2000/svg";
        Cone.prototype.getSurfaceRenderElement = function(ctx, renderer) {
          if (!renderer.isSvg) {
            return;
          }
          if (!this.surfaceSvgElement) {
            this.surfaceSvgElement = document.createElementNS(svgURI, "path");
            this.surfaceSvgElement.setAttribute("stroke-linecap", "round");
            this.surfaceSvgElement.setAttribute("stroke-linejoin", "round");
          }
          return this.surfaceSvgElement;
        };
        Cone.prototype.setSurfaceRenderPoint = function(index, point) {
          var renderPoint = this.surfacePathCommands[index].renderPoints[0];
          renderPoint.set(point);
        };
        return Cone;
      });
    }
  });

  // node_modules/zdog/js/box.js
  var require_box = __commonJS({
    "node_modules/zdog/js/box.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(
            require_boilerplate(),
            require_anchor(),
            require_shape(),
            require_rect()
          );
        } else {
          var Zdog2 = root.Zdog;
          Zdog2.Box = factory(Zdog2, Zdog2.Anchor, Zdog2.Shape, Zdog2.Rect);
        }
      })(exports, function factory(utils, Anchor, Shape, Rect) {
        var BoxRect = Rect.subclass();
        BoxRect.prototype.copyGraph = function() {
        };
        var TAU = utils.TAU;
        var faceNames = [
          "frontFace",
          "rearFace",
          "leftFace",
          "rightFace",
          "topFace",
          "bottomFace"
        ];
        var boxDefaults = utils.extend({}, Shape.defaults);
        delete boxDefaults.path;
        faceNames.forEach(function(faceName) {
          boxDefaults[faceName] = true;
        });
        utils.extend(boxDefaults, {
          width: 1,
          height: 1,
          depth: 1,
          fill: true
        });
        var Box = Anchor.subclass(boxDefaults);
        Box.prototype.create = function(options) {
          Anchor.prototype.create.call(this, options);
          this.updatePath();
          this.fill = this.fill;
        };
        Box.prototype.updatePath = function() {
          faceNames.forEach(function(faceName) {
            this[faceName] = this[faceName];
          }, this);
        };
        faceNames.forEach(function(faceName) {
          var _faceName = "_" + faceName;
          Object.defineProperty(Box.prototype, faceName, {
            get: function() {
              return this[_faceName];
            },
            set: function(value) {
              this[_faceName] = value;
              this.setFace(faceName, value);
            }
          });
        });
        Box.prototype.setFace = function(faceName, value) {
          var rectProperty = faceName + "Rect";
          var rect = this[rectProperty];
          if (!value) {
            this.removeChild(rect);
            return;
          }
          var options = this.getFaceOptions(faceName);
          options.color = typeof value == "string" ? value : this.color;
          if (rect) {
            rect.setOptions(options);
          } else {
            rect = this[rectProperty] = new BoxRect(options);
          }
          rect.updatePath();
          this.addChild(rect);
        };
        Box.prototype.getFaceOptions = function(faceName) {
          return {
            frontFace: {
              width: this.width,
              height: this.height,
              translate: { z: this.depth / 2 }
            },
            rearFace: {
              width: this.width,
              height: this.height,
              translate: { z: -this.depth / 2 },
              rotate: { y: TAU / 2 }
            },
            leftFace: {
              width: this.depth,
              height: this.height,
              translate: { x: -this.width / 2 },
              rotate: { y: -TAU / 4 }
            },
            rightFace: {
              width: this.depth,
              height: this.height,
              translate: { x: this.width / 2 },
              rotate: { y: TAU / 4 }
            },
            topFace: {
              width: this.width,
              height: this.depth,
              translate: { y: -this.height / 2 },
              rotate: { x: -TAU / 4 }
            },
            bottomFace: {
              width: this.width,
              height: this.depth,
              translate: { y: this.height / 2 },
              rotate: { x: TAU / 4 }
            }
          }[faceName];
        };
        var childProperties = [
          "color",
          "stroke",
          "fill",
          "backface",
          "front",
          "visible"
        ];
        childProperties.forEach(function(property) {
          var _prop = "_" + property;
          Object.defineProperty(Box.prototype, property, {
            get: function() {
              return this[_prop];
            },
            set: function(value) {
              this[_prop] = value;
              faceNames.forEach(function(faceName) {
                var rect = this[faceName + "Rect"];
                var isFaceColor = typeof this[faceName] == "string";
                var isColorUnderwrite = property == "color" && isFaceColor;
                if (rect && !isColorUnderwrite) {
                  rect[property] = value;
                }
              }, this);
            }
          });
        });
        return Box;
      });
    }
  });

  // node_modules/zdog/js/index.js
  var require_js = __commonJS({
    "node_modules/zdog/js/index.js"(exports, module) {
      (function(root, factory) {
        if (typeof module == "object" && module.exports) {
          module.exports = factory(
            require_boilerplate(),
            require_canvas_renderer(),
            require_svg_renderer(),
            require_vector(),
            require_anchor(),
            require_dragger(),
            require_illustration(),
            require_path_command(),
            require_shape(),
            require_group(),
            require_rect(),
            require_rounded_rect(),
            require_ellipse(),
            require_polygon(),
            require_hemisphere(),
            require_cylinder(),
            require_cone(),
            require_box()
          );
        } else if (typeof define == "function" && define.amd) {
          define("zdog", [], root.Zdog);
        }
      })(exports, function factory(Zdog2, CanvasRenderer, SvgRenderer, Vector, Anchor, Dragger, Illustration, PathCommand, Shape, Group, Rect, RoundedRect, Ellipse, Polygon, Hemisphere, Cylinder, Cone, Box) {
        Zdog2.CanvasRenderer = CanvasRenderer;
        Zdog2.SvgRenderer = SvgRenderer;
        Zdog2.Vector = Vector;
        Zdog2.Anchor = Anchor;
        Zdog2.Dragger = Dragger;
        Zdog2.Illustration = Illustration;
        Zdog2.PathCommand = PathCommand;
        Zdog2.Shape = Shape;
        Zdog2.Group = Group;
        Zdog2.Rect = Rect;
        Zdog2.RoundedRect = RoundedRect;
        Zdog2.Ellipse = Ellipse;
        Zdog2.Polygon = Polygon;
        Zdog2.Hemisphere = Hemisphere;
        Zdog2.Cylinder = Cylinder;
        Zdog2.Cone = Cone;
        Zdog2.Box = Box;
        return Zdog2;
      });
    }
  });

  // node_modules/glfx/glfx.js
  var require_glfx = __commonJS({
    "node_modules/glfx/glfx.js"(exports, module) {
      var fx2 = function() {
        function q(a2, d, c) {
          return Math.max(a2, Math.min(d, c));
        }
        function w(b) {
          return { _: b, loadContentsOf: function(b2) {
            a = this._.gl;
            this._.loadContentsOf(b2);
          }, destroy: function() {
            a = this._.gl;
            this._.destroy();
          } };
        }
        function A(a2) {
          return w(r.fromElement(a2));
        }
        function B(b, d) {
          var c = a.UNSIGNED_BYTE;
          if (a.getExtension("OES_texture_float") && a.getExtension("OES_texture_float_linear")) {
            var e = new r(100, 100, a.RGBA, a.FLOAT);
            try {
              e.drawTo(function() {
                c = a.FLOAT;
              });
            } catch (g) {
            }
            e.destroy();
          }
          this._.texture && this._.texture.destroy();
          this._.spareTexture && this._.spareTexture.destroy();
          this.width = b;
          this.height = d;
          this._.texture = new r(b, d, a.RGBA, c);
          this._.spareTexture = new r(b, d, a.RGBA, c);
          this._.extraTexture = this._.extraTexture || new r(0, 0, a.RGBA, c);
          this._.flippedShader = this._.flippedShader || new h(null, "uniform sampler2D texture;varying vec2 texCoord;void main(){gl_FragColor=texture2D(texture,vec2(texCoord.x,1.0-texCoord.y));}");
          this._.isInitialized = true;
        }
        function C(a2, d, c) {
          if (!this._.isInitialized || a2._.width != this.width || a2._.height != this.height) B.call(this, d ? d : a2._.width, c ? c : a2._.height);
          a2._.use();
          this._.texture.drawTo(function() {
            h.getDefaultShader().drawRect();
          });
          return this;
        }
        function D() {
          this._.texture.use();
          this._.flippedShader.drawRect();
          return this;
        }
        function f(a2, d, c, e) {
          (c || this._.texture).use();
          this._.spareTexture.drawTo(function() {
            a2.uniforms(d).drawRect();
          });
          this._.spareTexture.swapWith(e || this._.texture);
        }
        function E(a2) {
          a2.parentNode.insertBefore(this, a2);
          a2.parentNode.removeChild(a2);
          return this;
        }
        function F() {
          var b = new r(this._.texture.width, this._.texture.height, a.RGBA, a.UNSIGNED_BYTE);
          this._.texture.use();
          b.drawTo(function() {
            h.getDefaultShader().drawRect();
          });
          return w(b);
        }
        function G() {
          var b = this._.texture.width, d = this._.texture.height, c = new Uint8Array(4 * b * d);
          this._.texture.drawTo(function() {
            a.readPixels(0, 0, b, d, a.RGBA, a.UNSIGNED_BYTE, c);
          });
          return c;
        }
        function k(b) {
          return function() {
            a = this._.gl;
            return b.apply(this, arguments);
          };
        }
        function x(a2, d, c, e, g, n, l, p) {
          var m = c - g, h2 = e - n, f2 = l - g, k2 = p - n;
          g = a2 - c + g - l;
          n = d - e + n - p;
          var q2 = m * k2 - f2 * h2, f2 = (g * k2 - f2 * n) / q2, m = (m * n - g * h2) / q2;
          return [c - a2 + f2 * c, e - d + f2 * e, f2, l - a2 + m * l, p - d + m * p, m, a2, d, 1];
        }
        function y(a2) {
          var d = a2[0], c = a2[1], e = a2[2], g = a2[3], n = a2[4], l = a2[5], p = a2[6], m = a2[7];
          a2 = a2[8];
          var f2 = d * n * a2 - d * l * m - c * g * a2 + c * l * p + e * g * m - e * n * p;
          return [(n * a2 - l * m) / f2, (e * m - c * a2) / f2, (c * l - e * n) / f2, (l * p - g * a2) / f2, (d * a2 - e * p) / f2, (e * g - d * l) / f2, (g * m - n * p) / f2, (c * p - d * m) / f2, (d * n - c * g) / f2];
        }
        function z(a2) {
          var d = a2.length;
          this.xa = [];
          this.ya = [];
          this.u = [];
          this.y2 = [];
          a2.sort(function(a3, b) {
            return a3[0] - b[0];
          });
          for (var c = 0; c < d; c++) this.xa.push(a2[c][0]), this.ya.push(a2[c][1]);
          this.u[0] = 0;
          this.y2[0] = 0;
          for (c = 1; c < d - 1; ++c) {
            a2 = this.xa[c + 1] - this.xa[c - 1];
            var e = (this.xa[c] - this.xa[c - 1]) / a2, g = e * this.y2[c - 1] + 2;
            this.y2[c] = (e - 1) / g;
            this.u[c] = (6 * ((this.ya[c + 1] - this.ya[c]) / (this.xa[c + 1] - this.xa[c]) - (this.ya[c] - this.ya[c - 1]) / (this.xa[c] - this.xa[c - 1])) / a2 - e * this.u[c - 1]) / g;
          }
          this.y2[d - 1] = 0;
          for (c = d - 2; 0 <= c; --c) this.y2[c] = this.y2[c] * this.y2[c + 1] + this.u[c];
        }
        function u(a2, d) {
          return new h(null, a2 + "uniform sampler2D texture;uniform vec2 texSize;varying vec2 texCoord;void main(){vec2 coord=texCoord*texSize;" + d + "gl_FragColor=texture2D(texture,coord/texSize);vec2 clampedCoord=clamp(coord,vec2(0.0),texSize);if(coord!=clampedCoord){gl_FragColor.a*=max(0.0,1.0-length(coord-clampedCoord));}}");
        }
        function H(b) {
          a.noise = a.noise || new h(null, "uniform sampler2D texture;uniform float amount;varying vec2 texCoord;float rand(vec2 co){return fract(sin(dot(co.xy,vec2(12.9898,78.233)))*43758.5453);}void main(){vec4 color=texture2D(texture,texCoord);float diff=(rand(texCoord)-0.5)*amount;color.r+=diff;color.g+=diff;color.b+=diff;gl_FragColor=color;}");
          f.call(this, a.noise, { amount: q(0, b, 1) });
          return this;
        }
        function I(b) {
          a.vibrance = a.vibrance || new h(null, "uniform sampler2D texture;uniform float amount;varying vec2 texCoord;void main(){vec4 color=texture2D(texture,texCoord);float average=(color.r+color.g+color.b)/3.0;float mx=max(color.r,max(color.g,color.b));float amt=(mx-average)*(-amount*3.0);color.rgb=mix(color.rgb,vec3(mx),amt);gl_FragColor=color;}");
          f.call(this, a.vibrance, { amount: q(-1, b, 1) });
          return this;
        }
        function J(b, d) {
          a.vignette = a.vignette || new h(null, "uniform sampler2D texture;uniform float size;uniform float amount;varying vec2 texCoord;void main(){vec4 color=texture2D(texture,texCoord);float dist=distance(texCoord,vec2(0.5,0.5));color.rgb*=smoothstep(0.8,size*0.799,dist*(amount+size));gl_FragColor=color;}");
          f.call(this, a.vignette, { size: q(0, b, 1), amount: q(0, d, 1) });
          return this;
        }
        function K(b) {
          a.denoise = a.denoise || new h(null, "uniform sampler2D texture;uniform float exponent;uniform float strength;uniform vec2 texSize;varying vec2 texCoord;void main(){vec4 center=texture2D(texture,texCoord);vec4 color=vec4(0.0);float total=0.0;for(float x=-4.0;x<=4.0;x+=1.0){for(float y=-4.0;y<=4.0;y+=1.0){vec4 sample=texture2D(texture,texCoord+vec2(x,y)/texSize);float weight=1.0-abs(dot(sample.rgb-center.rgb,vec3(0.25)));weight=pow(weight,exponent);color+=sample*weight;total+=weight;}}gl_FragColor=color/total;}");
          for (var d = 0; 2 > d; d++) f.call(this, a.denoise, { exponent: Math.max(0, b), texSize: [this.width, this.height] });
          return this;
        }
        function L(b, d) {
          a.brightnessContrast = a.brightnessContrast || new h(null, "uniform sampler2D texture;uniform float brightness;uniform float contrast;varying vec2 texCoord;void main(){vec4 color=texture2D(texture,texCoord);color.rgb+=brightness;if(contrast>0.0){color.rgb=(color.rgb-0.5)/(1.0-contrast)+0.5;}else{color.rgb=(color.rgb-0.5)*(1.0+contrast)+0.5;}gl_FragColor=color;}");
          f.call(this, a.brightnessContrast, { brightness: q(-1, b, 1), contrast: q(-1, d, 1) });
          return this;
        }
        function t(a2) {
          a2 = new z(a2);
          for (var d = [], c = 0; 256 > c; c++) d.push(q(0, Math.floor(256 * a2.interpolate(c / 255)), 255));
          return d;
        }
        function M(b, d, c) {
          b = t(b);
          1 == arguments.length ? d = c = b : (d = t(d), c = t(c));
          for (var e = [], g = 0; 256 > g; g++) e.splice(e.length, 0, b[g], d[g], c[g], 255);
          this._.extraTexture.initFromBytes(256, 1, e);
          this._.extraTexture.use(1);
          a.curves = a.curves || new h(null, "uniform sampler2D texture;uniform sampler2D map;varying vec2 texCoord;void main(){vec4 color=texture2D(texture,texCoord);color.r=texture2D(map,vec2(color.r)).r;color.g=texture2D(map,vec2(color.g)).g;color.b=texture2D(map,vec2(color.b)).b;gl_FragColor=color;}");
          a.curves.textures({ map: 1 });
          f.call(this, a.curves, {});
          return this;
        }
        function N(b, d) {
          a.unsharpMask = a.unsharpMask || new h(null, "uniform sampler2D blurredTexture;uniform sampler2D originalTexture;uniform float strength;uniform float threshold;varying vec2 texCoord;void main(){vec4 blurred=texture2D(blurredTexture,texCoord);vec4 original=texture2D(originalTexture,texCoord);gl_FragColor=mix(blurred,original,1.0+strength);}");
          this._.extraTexture.ensureFormat(this._.texture);
          this._.texture.use();
          this._.extraTexture.drawTo(function() {
            h.getDefaultShader().drawRect();
          });
          this._.extraTexture.use(1);
          this.triangleBlur(b);
          a.unsharpMask.textures({ originalTexture: 1 });
          f.call(this, a.unsharpMask, { strength: d });
          this._.extraTexture.unuse(1);
          return this;
        }
        function O(b) {
          a.sepia = a.sepia || new h(null, "uniform sampler2D texture;uniform float amount;varying vec2 texCoord;void main(){vec4 color=texture2D(texture,texCoord);float r=color.r;float g=color.g;float b=color.b;color.r=min(1.0,(r*(1.0-(0.607*amount)))+(g*(0.769*amount))+(b*(0.189*amount)));color.g=min(1.0,(r*0.349*amount)+(g*(1.0-(0.314*amount)))+(b*0.168*amount));color.b=min(1.0,(r*0.272*amount)+(g*0.534*amount)+(b*(1.0-(0.869*amount))));gl_FragColor=color;}");
          f.call(this, a.sepia, { amount: q(0, b, 1) });
          return this;
        }
        function P(b, d) {
          a.hueSaturation = a.hueSaturation || new h(null, "uniform sampler2D texture;uniform float hue;uniform float saturation;varying vec2 texCoord;void main(){vec4 color=texture2D(texture,texCoord);float angle=hue*3.14159265;float s=sin(angle),c=cos(angle);vec3 weights=(vec3(2.0*c,-sqrt(3.0)*s-c,sqrt(3.0)*s-c)+1.0)/3.0;float len=length(color.rgb);color.rgb=vec3(dot(color.rgb,weights.xyz),dot(color.rgb,weights.zxy),dot(color.rgb,weights.yzx));float average=(color.r+color.g+color.b)/3.0;if(saturation>0.0){color.rgb+=(average-color.rgb)*(1.0-1.0/(1.001-saturation));}else{color.rgb+=(average-color.rgb)*(-saturation);}gl_FragColor=color;}");
          f.call(this, a.hueSaturation, { hue: q(-1, b, 1), saturation: q(-1, d, 1) });
          return this;
        }
        function Q(b, d, c) {
          a.zoomBlur = a.zoomBlur || new h(null, "uniform sampler2D texture;uniform vec2 center;uniform float strength;uniform vec2 texSize;varying vec2 texCoord;" + s + "void main(){vec4 color=vec4(0.0);float total=0.0;vec2 toCenter=center-texCoord*texSize;float offset=random(vec3(12.9898,78.233,151.7182),0.0);for(float t=0.0;t<=40.0;t++){float percent=(t+offset)/40.0;float weight=4.0*(percent-percent*percent);vec4 sample=texture2D(texture,texCoord+toCenter*percent*strength/texSize);sample.rgb*=sample.a;color+=sample*weight;total+=weight;}gl_FragColor=color/total;gl_FragColor.rgb/=gl_FragColor.a+0.00001;}");
          f.call(this, a.zoomBlur, { center: [b, d], strength: c, texSize: [this.width, this.height] });
          return this;
        }
        function R(b, d, c, e, g, n) {
          a.tiltShift = a.tiltShift || new h(null, "uniform sampler2D texture;uniform float blurRadius;uniform float gradientRadius;uniform vec2 start;uniform vec2 end;uniform vec2 delta;uniform vec2 texSize;varying vec2 texCoord;" + s + "void main(){vec4 color=vec4(0.0);float total=0.0;float offset=random(vec3(12.9898,78.233,151.7182),0.0);vec2 normal=normalize(vec2(start.y-end.y,end.x-start.x));float radius=smoothstep(0.0,1.0,abs(dot(texCoord*texSize-start,normal))/gradientRadius)*blurRadius;for(float t=-30.0;t<=30.0;t++){float percent=(t+offset-0.5)/30.0;float weight=1.0-abs(percent);vec4 sample=texture2D(texture,texCoord+delta/texSize*percent*radius);sample.rgb*=sample.a;color+=sample*weight;total+=weight;}gl_FragColor=color/total;gl_FragColor.rgb/=gl_FragColor.a+0.00001;}");
          var l = c - b, p = e - d, m = Math.sqrt(l * l + p * p);
          f.call(this, a.tiltShift, { blurRadius: g, gradientRadius: n, start: [b, d], end: [c, e], delta: [l / m, p / m], texSize: [this.width, this.height] });
          f.call(this, a.tiltShift, { blurRadius: g, gradientRadius: n, start: [b, d], end: [c, e], delta: [-p / m, l / m], texSize: [this.width, this.height] });
          return this;
        }
        function S(b, d, c) {
          a.lensBlurPrePass = a.lensBlurPrePass || new h(null, "uniform sampler2D texture;uniform float power;varying vec2 texCoord;void main(){vec4 color=texture2D(texture,texCoord);color=pow(color,vec4(power));gl_FragColor=vec4(color);}");
          var e = "uniform sampler2D texture0;uniform sampler2D texture1;uniform vec2 delta0;uniform vec2 delta1;uniform float power;varying vec2 texCoord;" + s + "vec4 sample(vec2 delta){float offset=random(vec3(delta,151.7182),0.0);vec4 color=vec4(0.0);float total=0.0;for(float t=0.0;t<=30.0;t++){float percent=(t+offset)/30.0;color+=texture2D(texture0,texCoord+delta*percent);total+=1.0;}return color/total;}";
          a.lensBlur0 = a.lensBlur0 || new h(null, e + "void main(){gl_FragColor=sample(delta0);}");
          a.lensBlur1 = a.lensBlur1 || new h(null, e + "void main(){gl_FragColor=(sample(delta0)+sample(delta1))*0.5;}");
          a.lensBlur2 = a.lensBlur2 || new h(null, e + "void main(){vec4 color=(sample(delta0)+2.0*texture2D(texture1,texCoord))/3.0;gl_FragColor=pow(color,vec4(power));}").textures({ texture1: 1 });
          for (var e = [], g = 0; 3 > g; g++) {
            var n = c + 2 * g * Math.PI / 3;
            e.push([b * Math.sin(n) / this.width, b * Math.cos(n) / this.height]);
          }
          b = Math.pow(10, q(-1, d, 1));
          f.call(this, a.lensBlurPrePass, { power: b });
          this._.extraTexture.ensureFormat(this._.texture);
          f.call(this, a.lensBlur0, { delta0: e[0] }, this._.texture, this._.extraTexture);
          f.call(this, a.lensBlur1, { delta0: e[1], delta1: e[2] }, this._.extraTexture, this._.extraTexture);
          f.call(this, a.lensBlur0, { delta0: e[1] });
          this._.extraTexture.use(1);
          f.call(this, a.lensBlur2, { power: 1 / b, delta0: e[2] });
          return this;
        }
        function T(b) {
          a.triangleBlur = a.triangleBlur || new h(null, "uniform sampler2D texture;uniform vec2 delta;varying vec2 texCoord;" + s + "void main(){vec4 color=vec4(0.0);float total=0.0;float offset=random(vec3(12.9898,78.233,151.7182),0.0);for(float t=-30.0;t<=30.0;t++){float percent=(t+offset-0.5)/30.0;float weight=1.0-abs(percent);vec4 sample=texture2D(texture,texCoord+delta*percent);sample.rgb*=sample.a;color+=sample*weight;total+=weight;}gl_FragColor=color/total;gl_FragColor.rgb/=gl_FragColor.a+0.00001;}");
          f.call(this, a.triangleBlur, { delta: [b / this.width, 0] });
          f.call(this, a.triangleBlur, { delta: [0, b / this.height] });
          return this;
        }
        function U(b) {
          a.edgeWork1 = a.edgeWork1 || new h(null, "uniform sampler2D texture;uniform vec2 delta;varying vec2 texCoord;" + s + "void main(){vec2 color=vec2(0.0);vec2 total=vec2(0.0);float offset=random(vec3(12.9898,78.233,151.7182),0.0);for(float t=-30.0;t<=30.0;t++){float percent=(t+offset-0.5)/30.0;float weight=1.0-abs(percent);vec3 sample=texture2D(texture,texCoord+delta*percent).rgb;float average=(sample.r+sample.g+sample.b)/3.0;color.x+=average*weight;total.x+=weight;if(abs(t)<15.0){weight=weight*2.0-1.0;color.y+=average*weight;total.y+=weight;}}gl_FragColor=vec4(color/total,0.0,1.0);}");
          a.edgeWork2 = a.edgeWork2 || new h(null, "uniform sampler2D texture;uniform vec2 delta;varying vec2 texCoord;" + s + "void main(){vec2 color=vec2(0.0);vec2 total=vec2(0.0);float offset=random(vec3(12.9898,78.233,151.7182),0.0);for(float t=-30.0;t<=30.0;t++){float percent=(t+offset-0.5)/30.0;float weight=1.0-abs(percent);vec2 sample=texture2D(texture,texCoord+delta*percent).xy;color.x+=sample.x*weight;total.x+=weight;if(abs(t)<15.0){weight=weight*2.0-1.0;color.y+=sample.y*weight;total.y+=weight;}}float c=clamp(10000.0*(color.y/total.y-color.x/total.x)+0.5,0.0,1.0);gl_FragColor=vec4(c,c,c,1.0);}");
          f.call(this, a.edgeWork1, { delta: [b / this.width, 0] });
          f.call(this, a.edgeWork2, { delta: [0, b / this.height] });
          return this;
        }
        function V(b, d, c) {
          a.hexagonalPixelate = a.hexagonalPixelate || new h(null, "uniform sampler2D texture;uniform vec2 center;uniform float scale;uniform vec2 texSize;varying vec2 texCoord;void main(){vec2 tex=(texCoord*texSize-center)/scale;tex.y/=0.866025404;tex.x-=tex.y*0.5;vec2 a;if(tex.x+tex.y-floor(tex.x)-floor(tex.y)<1.0)a=vec2(floor(tex.x),floor(tex.y));else a=vec2(ceil(tex.x),ceil(tex.y));vec2 b=vec2(ceil(tex.x),floor(tex.y));vec2 c=vec2(floor(tex.x),ceil(tex.y));vec3 TEX=vec3(tex.x,tex.y,1.0-tex.x-tex.y);vec3 A=vec3(a.x,a.y,1.0-a.x-a.y);vec3 B=vec3(b.x,b.y,1.0-b.x-b.y);vec3 C=vec3(c.x,c.y,1.0-c.x-c.y);float alen=length(TEX-A);float blen=length(TEX-B);float clen=length(TEX-C);vec2 choice;if(alen<blen){if(alen<clen)choice=a;else choice=c;}else{if(blen<clen)choice=b;else choice=c;}choice.x+=choice.y*0.5;choice.y*=0.866025404;choice*=scale/texSize;gl_FragColor=texture2D(texture,choice+center/texSize);}");
          f.call(this, a.hexagonalPixelate, { center: [b, d], scale: c, texSize: [this.width, this.height] });
          return this;
        }
        function W(b, d, c, e) {
          a.colorHalftone = a.colorHalftone || new h(null, "uniform sampler2D texture;uniform vec2 center;uniform float angle;uniform float scale;uniform vec2 texSize;varying vec2 texCoord;float pattern(float angle){float s=sin(angle),c=cos(angle);vec2 tex=texCoord*texSize-center;vec2 point=vec2(c*tex.x-s*tex.y,s*tex.x+c*tex.y)*scale;return(sin(point.x)*sin(point.y))*4.0;}void main(){vec4 color=texture2D(texture,texCoord);vec3 cmy=1.0-color.rgb;float k=min(cmy.x,min(cmy.y,cmy.z));cmy=(cmy-k)/(1.0-k);cmy=clamp(cmy*10.0-3.0+vec3(pattern(angle+0.26179),pattern(angle+1.30899),pattern(angle)),0.0,1.0);k=clamp(k*10.0-5.0+pattern(angle+0.78539),0.0,1.0);gl_FragColor=vec4(1.0-cmy-k,color.a);}");
          f.call(this, a.colorHalftone, { center: [b, d], angle: c, scale: Math.PI / e, texSize: [this.width, this.height] });
          return this;
        }
        function X(b) {
          a.ink = a.ink || new h(null, "uniform sampler2D texture;uniform float strength;uniform vec2 texSize;varying vec2 texCoord;void main(){vec2 dx=vec2(1.0/texSize.x,0.0);vec2 dy=vec2(0.0,1.0/texSize.y);vec4 color=texture2D(texture,texCoord);float bigTotal=0.0;float smallTotal=0.0;vec3 bigAverage=vec3(0.0);vec3 smallAverage=vec3(0.0);for(float x=-2.0;x<=2.0;x+=1.0){for(float y=-2.0;y<=2.0;y+=1.0){vec3 sample=texture2D(texture,texCoord+dx*x+dy*y).rgb;bigAverage+=sample;bigTotal+=1.0;if(abs(x)+abs(y)<2.0){smallAverage+=sample;smallTotal+=1.0;}}}vec3 edge=max(vec3(0.0),bigAverage/bigTotal-smallAverage/smallTotal);gl_FragColor=vec4(color.rgb-dot(edge,edge)*strength*100000.0,color.a);}");
          f.call(this, a.ink, { strength: b * b * b * b * b, texSize: [this.width, this.height] });
          return this;
        }
        function Y(b, d, c, e) {
          a.dotScreen = a.dotScreen || new h(null, "uniform sampler2D texture;uniform vec2 center;uniform float angle;uniform float scale;uniform vec2 texSize;varying vec2 texCoord;float pattern(){float s=sin(angle),c=cos(angle);vec2 tex=texCoord*texSize-center;vec2 point=vec2(c*tex.x-s*tex.y,s*tex.x+c*tex.y)*scale;return(sin(point.x)*sin(point.y))*4.0;}void main(){vec4 color=texture2D(texture,texCoord);float average=(color.r+color.g+color.b)/3.0;gl_FragColor=vec4(vec3(average*10.0-5.0+pattern()),color.a);}");
          f.call(this, a.dotScreen, { center: [b, d], angle: c, scale: Math.PI / e, texSize: [this.width, this.height] });
          return this;
        }
        function Z(b, d, c) {
          a.matrixWarp = a.matrixWarp || u("uniform mat3 matrix;uniform bool useTextureSpace;", "if(useTextureSpace)coord=coord/texSize*2.0-1.0;vec3 warp=matrix*vec3(coord,1.0);coord=warp.xy/warp.z;if(useTextureSpace)coord=(coord*0.5+0.5)*texSize;");
          b = Array.prototype.concat.apply([], b);
          if (4 == b.length) b = [b[0], b[1], 0, b[2], b[3], 0, 0, 0, 1];
          else if (9 != b.length) throw "can only warp with 2x2 or 3x3 matrix";
          f.call(this, a.matrixWarp, { matrix: d ? y(b) : b, texSize: [this.width, this.height], useTextureSpace: c | 0 });
          return this;
        }
        function $(b, d, c, e) {
          a.swirl = a.swirl || u("uniform float radius;uniform float angle;uniform vec2 center;", "coord-=center;float distance=length(coord);if(distance<radius){float percent=(radius-distance)/radius;float theta=percent*percent*angle;float s=sin(theta);float c=cos(theta);coord=vec2(coord.x*c-coord.y*s,coord.x*s+coord.y*c);}coord+=center;");
          f.call(this, a.swirl, { radius: c, center: [b, d], angle: e, texSize: [this.width, this.height] });
          return this;
        }
        function aa(b, d, c, e) {
          a.bulgePinch = a.bulgePinch || u("uniform float radius;uniform float strength;uniform vec2 center;", "coord-=center;float distance=length(coord);if(distance<radius){float percent=distance/radius;if(strength>0.0){coord*=mix(1.0,smoothstep(0.0,radius/distance,percent),strength*0.75);}else{coord*=mix(1.0,pow(percent,1.0+strength*0.75)*radius/distance,1.0-percent);}}coord+=center;");
          f.call(this, a.bulgePinch, { radius: c, strength: q(-1, e, 1), center: [b, d], texSize: [this.width, this.height] });
          return this;
        }
        function ba(a2, d) {
          var c = x.apply(null, d), e = x.apply(null, a2), c = y(c);
          return this.matrixWarp([c[0] * e[0] + c[1] * e[3] + c[2] * e[6], c[0] * e[1] + c[1] * e[4] + c[2] * e[7], c[0] * e[2] + c[1] * e[5] + c[2] * e[8], c[3] * e[0] + c[4] * e[3] + c[5] * e[6], c[3] * e[1] + c[4] * e[4] + c[5] * e[7], c[3] * e[2] + c[4] * e[5] + c[5] * e[8], c[6] * e[0] + c[7] * e[3] + c[8] * e[6], c[6] * e[1] + c[7] * e[4] + c[8] * e[7], c[6] * e[2] + c[7] * e[5] + c[8] * e[8]]);
        }
        var v = {};
        (function() {
          function a2(b) {
            if (!b.getExtension("OES_texture_float")) return false;
            var c2 = b.createFramebuffer(), e2 = b.createTexture();
            b.bindTexture(b.TEXTURE_2D, e2);
            b.texParameteri(b.TEXTURE_2D, b.TEXTURE_MAG_FILTER, b.NEAREST);
            b.texParameteri(b.TEXTURE_2D, b.TEXTURE_MIN_FILTER, b.NEAREST);
            b.texParameteri(b.TEXTURE_2D, b.TEXTURE_WRAP_S, b.CLAMP_TO_EDGE);
            b.texParameteri(b.TEXTURE_2D, b.TEXTURE_WRAP_T, b.CLAMP_TO_EDGE);
            b.texImage2D(b.TEXTURE_2D, 0, b.RGBA, 1, 1, 0, b.RGBA, b.UNSIGNED_BYTE, null);
            b.bindFramebuffer(b.FRAMEBUFFER, c2);
            b.framebufferTexture2D(
              b.FRAMEBUFFER,
              b.COLOR_ATTACHMENT0,
              b.TEXTURE_2D,
              e2,
              0
            );
            c2 = b.createTexture();
            b.bindTexture(b.TEXTURE_2D, c2);
            b.texParameteri(b.TEXTURE_2D, b.TEXTURE_MAG_FILTER, b.LINEAR);
            b.texParameteri(b.TEXTURE_2D, b.TEXTURE_MIN_FILTER, b.LINEAR);
            b.texParameteri(b.TEXTURE_2D, b.TEXTURE_WRAP_S, b.CLAMP_TO_EDGE);
            b.texParameteri(b.TEXTURE_2D, b.TEXTURE_WRAP_T, b.CLAMP_TO_EDGE);
            b.texImage2D(b.TEXTURE_2D, 0, b.RGBA, 2, 2, 0, b.RGBA, b.FLOAT, new Float32Array([2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]));
            var e2 = b.createProgram(), d2 = b.createShader(b.VERTEX_SHADER), g2 = b.createShader(b.FRAGMENT_SHADER);
            b.shaderSource(d2, "attribute vec2 vertex;void main(){gl_Position=vec4(vertex,0.0,1.0);}");
            b.shaderSource(g2, "uniform sampler2D texture;void main(){gl_FragColor=texture2D(texture,vec2(0.5));}");
            b.compileShader(d2);
            b.compileShader(g2);
            b.attachShader(e2, d2);
            b.attachShader(e2, g2);
            b.linkProgram(e2);
            d2 = b.createBuffer();
            b.bindBuffer(b.ARRAY_BUFFER, d2);
            b.bufferData(b.ARRAY_BUFFER, new Float32Array([0, 0]), b.STREAM_DRAW);
            b.enableVertexAttribArray(0);
            b.vertexAttribPointer(0, 2, b.FLOAT, false, 0, 0);
            d2 = new Uint8Array(4);
            b.useProgram(e2);
            b.viewport(0, 0, 1, 1);
            b.bindTexture(b.TEXTURE_2D, c2);
            b.drawArrays(b.POINTS, 0, 1);
            b.readPixels(0, 0, 1, 1, b.RGBA, b.UNSIGNED_BYTE, d2);
            return 127 === d2[0] || 128 === d2[0];
          }
          function d() {
          }
          function c(a3) {
            "OES_texture_float_linear" === a3 ? (void 0 === this.$OES_texture_float_linear$ && Object.defineProperty(this, "$OES_texture_float_linear$", { enumerable: false, configurable: false, writable: false, value: new d() }), a3 = this.$OES_texture_float_linear$) : a3 = l.call(this, a3);
            return a3;
          }
          function e() {
            var a3 = f2.call(this);
            -1 === a3.indexOf("OES_texture_float_linear") && a3.push("OES_texture_float_linear");
            return a3;
          }
          try {
            var g = document.createElement("canvas").getContext("experimental-webgl");
          } catch (n) {
          }
          if (g && -1 === g.getSupportedExtensions().indexOf("OES_texture_float_linear") && a2(g)) {
            var l = WebGLRenderingContext.prototype.getExtension, f2 = WebGLRenderingContext.prototype.getSupportedExtensions;
            WebGLRenderingContext.prototype.getExtension = c;
            WebGLRenderingContext.prototype.getSupportedExtensions = e;
          }
        })();
        var a;
        v.canvas = function() {
          var b = document.createElement("canvas");
          try {
            a = b.getContext("experimental-webgl", { premultipliedAlpha: false });
          } catch (d) {
            a = null;
          }
          if (!a) throw "This browser does not support WebGL";
          b._ = { gl: a, isInitialized: false, texture: null, spareTexture: null, flippedShader: null };
          b.texture = k(A);
          b.draw = k(C);
          b.update = k(D);
          b.replace = k(E);
          b.contents = k(F);
          b.getPixelArray = k(G);
          b.brightnessContrast = k(L);
          b.hexagonalPixelate = k(V);
          b.hueSaturation = k(P);
          b.colorHalftone = k(W);
          b.triangleBlur = k(T);
          b.unsharpMask = k(N);
          b.perspective = k(ba);
          b.matrixWarp = k(Z);
          b.bulgePinch = k(aa);
          b.tiltShift = k(R);
          b.dotScreen = k(Y);
          b.edgeWork = k(U);
          b.lensBlur = k(S);
          b.zoomBlur = k(Q);
          b.noise = k(H);
          b.denoise = k(K);
          b.curves = k(M);
          b.swirl = k($);
          b.ink = k(X);
          b.vignette = k(J);
          b.vibrance = k(I);
          b.sepia = k(O);
          return b;
        };
        v.splineInterpolate = t;
        var r = function() {
          function b(b2, c2, d2, l) {
            this.gl = a;
            this.id = a.createTexture();
            this.width = b2;
            this.height = c2;
            this.format = d2;
            this.type = l;
            a.bindTexture(a.TEXTURE_2D, this.id);
            a.texParameteri(a.TEXTURE_2D, a.TEXTURE_MAG_FILTER, a.LINEAR);
            a.texParameteri(
              a.TEXTURE_2D,
              a.TEXTURE_MIN_FILTER,
              a.LINEAR
            );
            a.texParameteri(a.TEXTURE_2D, a.TEXTURE_WRAP_S, a.CLAMP_TO_EDGE);
            a.texParameteri(a.TEXTURE_2D, a.TEXTURE_WRAP_T, a.CLAMP_TO_EDGE);
            b2 && c2 && a.texImage2D(a.TEXTURE_2D, 0, this.format, b2, c2, 0, this.format, this.type, null);
          }
          function d(a2) {
            null == c && (c = document.createElement("canvas"));
            c.width = a2.width;
            c.height = a2.height;
            a2 = c.getContext("2d");
            a2.clearRect(0, 0, c.width, c.height);
            return a2;
          }
          b.fromElement = function(c2) {
            var d2 = new b(0, 0, a.RGBA, a.UNSIGNED_BYTE);
            d2.loadContentsOf(c2);
            return d2;
          };
          b.prototype.loadContentsOf = function(b2) {
            this.width = b2.width || b2.videoWidth;
            this.height = b2.height || b2.videoHeight;
            a.bindTexture(a.TEXTURE_2D, this.id);
            a.texImage2D(a.TEXTURE_2D, 0, this.format, this.format, this.type, b2);
          };
          b.prototype.initFromBytes = function(b2, c2, d2) {
            this.width = b2;
            this.height = c2;
            this.format = a.RGBA;
            this.type = a.UNSIGNED_BYTE;
            a.bindTexture(a.TEXTURE_2D, this.id);
            a.texImage2D(a.TEXTURE_2D, 0, a.RGBA, b2, c2, 0, a.RGBA, this.type, new Uint8Array(d2));
          };
          b.prototype.destroy = function() {
            a.deleteTexture(this.id);
            this.id = null;
          };
          b.prototype.use = function(b2) {
            a.activeTexture(a.TEXTURE0 + (b2 || 0));
            a.bindTexture(a.TEXTURE_2D, this.id);
          };
          b.prototype.unuse = function(b2) {
            a.activeTexture(a.TEXTURE0 + (b2 || 0));
            a.bindTexture(a.TEXTURE_2D, null);
          };
          b.prototype.ensureFormat = function(b2, c2, d2, l) {
            if (1 == arguments.length) {
              var f2 = arguments[0];
              b2 = f2.width;
              c2 = f2.height;
              d2 = f2.format;
              l = f2.type;
            }
            if (b2 != this.width || c2 != this.height || d2 != this.format || l != this.type) this.width = b2, this.height = c2, this.format = d2, this.type = l, a.bindTexture(a.TEXTURE_2D, this.id), a.texImage2D(a.TEXTURE_2D, 0, this.format, b2, c2, 0, this.format, this.type, null);
          };
          b.prototype.drawTo = function(b2) {
            a.framebuffer = a.framebuffer || a.createFramebuffer();
            a.bindFramebuffer(a.FRAMEBUFFER, a.framebuffer);
            a.framebufferTexture2D(a.FRAMEBUFFER, a.COLOR_ATTACHMENT0, a.TEXTURE_2D, this.id, 0);
            if (a.checkFramebufferStatus(a.FRAMEBUFFER) !== a.FRAMEBUFFER_COMPLETE) throw Error("incomplete framebuffer");
            a.viewport(0, 0, this.width, this.height);
            b2();
            a.bindFramebuffer(a.FRAMEBUFFER, null);
          };
          var c = null;
          b.prototype.fillUsingCanvas = function(b2) {
            b2(d(this));
            this.format = a.RGBA;
            this.type = a.UNSIGNED_BYTE;
            a.bindTexture(
              a.TEXTURE_2D,
              this.id
            );
            a.texImage2D(a.TEXTURE_2D, 0, a.RGBA, a.RGBA, a.UNSIGNED_BYTE, c);
            return this;
          };
          b.prototype.toImage = function(b2) {
            this.use();
            h.getDefaultShader().drawRect();
            var g = 4 * this.width * this.height, f2 = new Uint8Array(g), l = d(this), p = l.createImageData(this.width, this.height);
            a.readPixels(0, 0, this.width, this.height, a.RGBA, a.UNSIGNED_BYTE, f2);
            for (var m = 0; m < g; m++) p.data[m] = f2[m];
            l.putImageData(p, 0, 0);
            b2.src = c.toDataURL();
          };
          b.prototype.swapWith = function(a2) {
            var b2;
            b2 = a2.id;
            a2.id = this.id;
            this.id = b2;
            b2 = a2.width;
            a2.width = this.width;
            this.width = b2;
            b2 = a2.height;
            a2.height = this.height;
            this.height = b2;
            b2 = a2.format;
            a2.format = this.format;
            this.format = b2;
          };
          return b;
        }();
        z.prototype.interpolate = function(a2) {
          for (var d = 0, c = this.ya.length - 1; 1 < c - d; ) {
            var e = c + d >> 1;
            this.xa[e] > a2 ? c = e : d = e;
          }
          var e = this.xa[c] - this.xa[d], g = (this.xa[c] - a2) / e;
          a2 = (a2 - this.xa[d]) / e;
          return g * this.ya[d] + a2 * this.ya[c] + ((g * g * g - g) * this.y2[d] + (a2 * a2 * a2 - a2) * this.y2[c]) * e * e / 6;
        };
        var h = function() {
          function b(b2, c2) {
            var d2 = a.createShader(b2);
            a.shaderSource(d2, c2);
            a.compileShader(d2);
            if (!a.getShaderParameter(d2, a.COMPILE_STATUS)) throw "compile error: " + a.getShaderInfoLog(d2);
            return d2;
          }
          function d(d2, f2) {
            this.texCoordAttribute = this.vertexAttribute = null;
            this.program = a.createProgram();
            d2 = d2 || c;
            f2 = f2 || e;
            f2 = "precision highp float;" + f2;
            a.attachShader(this.program, b(a.VERTEX_SHADER, d2));
            a.attachShader(this.program, b(a.FRAGMENT_SHADER, f2));
            a.linkProgram(this.program);
            if (!a.getProgramParameter(this.program, a.LINK_STATUS)) throw "link error: " + a.getProgramInfoLog(this.program);
          }
          var c = "attribute vec2 vertex;attribute vec2 _texCoord;varying vec2 texCoord;void main(){texCoord=_texCoord;gl_Position=vec4(vertex*2.0-1.0,0.0,1.0);}", e = "uniform sampler2D texture;varying vec2 texCoord;void main(){gl_FragColor=texture2D(texture,texCoord);}";
          d.prototype.destroy = function() {
            a.deleteProgram(this.program);
            this.program = null;
          };
          d.prototype.uniforms = function(b2) {
            a.useProgram(this.program);
            for (var c2 in b2) if (b2.hasOwnProperty(c2)) {
              var d2 = a.getUniformLocation(this.program, c2);
              if (null !== d2) {
                var e2 = b2[c2];
                if ("[object Array]" == Object.prototype.toString.call(e2)) switch (e2.length) {
                  case 1:
                    a.uniform1fv(d2, new Float32Array(e2));
                    break;
                  case 2:
                    a.uniform2fv(d2, new Float32Array(e2));
                    break;
                  case 3:
                    a.uniform3fv(d2, new Float32Array(e2));
                    break;
                  case 4:
                    a.uniform4fv(d2, new Float32Array(e2));
                    break;
                  case 9:
                    a.uniformMatrix3fv(d2, false, new Float32Array(e2));
                    break;
                  case 16:
                    a.uniformMatrix4fv(d2, false, new Float32Array(e2));
                    break;
                  default:
                    throw `dont't know how to load uniform "` + c2 + '" of length ' + e2.length;
                }
                else if ("[object Number]" == Object.prototype.toString.call(e2)) a.uniform1f(d2, e2);
                else throw 'attempted to set uniform "' + c2 + '" to invalid value ' + (e2 || "undefined").toString();
              }
            }
            return this;
          };
          d.prototype.textures = function(b2) {
            a.useProgram(this.program);
            for (var c2 in b2) b2.hasOwnProperty(c2) && a.uniform1i(a.getUniformLocation(this.program, c2), b2[c2]);
            return this;
          };
          d.prototype.drawRect = function(b2, c2, d2, e2) {
            var f2 = a.getParameter(a.VIEWPORT);
            c2 = void 0 !== c2 ? (c2 - f2[1]) / f2[3] : 0;
            b2 = void 0 !== b2 ? (b2 - f2[0]) / f2[2] : 0;
            d2 = void 0 !== d2 ? (d2 - f2[0]) / f2[2] : 1;
            e2 = void 0 !== e2 ? (e2 - f2[1]) / f2[3] : 1;
            null == a.vertexBuffer && (a.vertexBuffer = a.createBuffer());
            a.bindBuffer(a.ARRAY_BUFFER, a.vertexBuffer);
            a.bufferData(a.ARRAY_BUFFER, new Float32Array([
              b2,
              c2,
              b2,
              e2,
              d2,
              c2,
              d2,
              e2
            ]), a.STATIC_DRAW);
            null == a.texCoordBuffer && (a.texCoordBuffer = a.createBuffer(), a.bindBuffer(a.ARRAY_BUFFER, a.texCoordBuffer), a.bufferData(a.ARRAY_BUFFER, new Float32Array([0, 0, 0, 1, 1, 0, 1, 1]), a.STATIC_DRAW));
            null == this.vertexAttribute && (this.vertexAttribute = a.getAttribLocation(this.program, "vertex"), a.enableVertexAttribArray(this.vertexAttribute));
            null == this.texCoordAttribute && (this.texCoordAttribute = a.getAttribLocation(this.program, "_texCoord"), a.enableVertexAttribArray(this.texCoordAttribute));
            a.useProgram(this.program);
            a.bindBuffer(a.ARRAY_BUFFER, a.vertexBuffer);
            a.vertexAttribPointer(this.vertexAttribute, 2, a.FLOAT, false, 0, 0);
            a.bindBuffer(a.ARRAY_BUFFER, a.texCoordBuffer);
            a.vertexAttribPointer(this.texCoordAttribute, 2, a.FLOAT, false, 0, 0);
            a.drawArrays(a.TRIANGLE_STRIP, 0, 4);
          };
          d.getDefaultShader = function() {
            a.defaultShader = a.defaultShader || new d();
            return a.defaultShader;
          };
          return d;
        }(), s = "float random(vec3 scale,float seed){return fract(sin(dot(gl_FragCoord.xyz+seed,scale))*43758.5453+seed);}";
        return v;
      }();
      "object" === typeof module ? module.exports = fx2 : window.fx = fx2;
    }
  });

  // src/main.js
  var import_zdog = __toESM(require_js(), 1);
  var import_glfx = __toESM(require_glfx(), 1);

  // node_modules/@vfx-js/core/lib/esm/constants.js
  var DEFAULT_VERTEX_SHADER = `
precision highp float;
in vec3 position;
void main() {
    gl_Position = vec4(position, 1.0);
}
`;
  var DEFAULT_VERTEX_SHADER_100 = `
precision highp float;
attribute vec3 position;
void main() {
    gl_Position = vec4(position, 1.0);
}
`;
  var COPY_FRAGMENT_SHADER = `
precision highp float;
uniform vec2 offset;
uniform vec2 resolution;
uniform sampler2D src;
out vec4 outColor;
void main() {
    vec2 uv = (gl_FragCoord.xy - offset) / resolution;
    if (uv.x < 0. || uv.x > 1. || uv.y < 0. || uv.y > 1.) {
        discard;
    }
    outColor = texture(src, uv);
}
`;
  var COMMON_HEADER = `precision highp float;
uniform vec2 resolution;
uniform vec2 offset;
uniform float time;
uniform bool autoCrop;
uniform sampler2D src;
out vec4 outColor;
`;
  var READ_TEX = `vec4 readTex(sampler2D tex, vec2 uv) {
    if (autoCrop && (uv.x < 0. || uv.x > 1. || uv.y < 0. || uv.y > 1.)) {
        return vec4(0);
    }
    return texture(tex, uv);
}`;
  var shaders = {
    none: COPY_FRAGMENT_SHADER,
    uvGradient: `
    ${COMMON_HEADER}
    ${READ_TEX}

    void main() {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        outColor = vec4(uv, sin(time) * .5 + .5, 1);

        vec4 img = readTex(src, uv);
        outColor *= smoothstep(0., 1., img.a);
    }
    `,
    rainbow: `
    ${COMMON_HEADER}
    ${READ_TEX}

    vec3 hsv2rgb(vec3 c) {
        vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
        vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
        return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
    }

    vec3 rgb2hsv(vec3 c) {
        vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
        vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
        vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

        float d = q.x - min(q.w, q.y);
        float e = 1.0e-10;
        return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
    }

    vec3 hueShift(vec3 rgb, float t) {
        vec3 hsv = rgb2hsv(rgb);
        hsv.x = fract(hsv.x + t);
        return hsv2rgb(hsv);
    }

    void main() {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        vec2 uv2 = uv;
        uv2.x *= resolution.x / resolution.y;

        float x = (uv2.x - uv2.y) - fract(time);

        vec4 img = readTex(src, uv);
        float gray = length(img.rgb);

        img.rgb = vec3(hueShift(vec3(1,0,0), x) * gray);

        outColor = img;
    }
    `,
    glitch: `
    ${COMMON_HEADER}
    ${READ_TEX}

    float nn(float y, float t) {
        float n = (
            sin(y * .07 + t * 8. + sin(y * .5 + t * 10.)) +
            sin(y * .7 + t * 2. + sin(y * .3 + t * 8.)) * .7 +
            sin(y * 1.1 + t * 2.8) * .4
        );

        n += sin(y * 124. + t * 100.7) * sin(y * 877. - t * 38.8) * .3;

        return n;
    }

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        vec4 color = readTex(src, uv);

        float t = mod(time, 3.14 * 10.);

        // Seed value
        float v = fract(sin(t * 2.) * 700.);

        if (abs(nn(uv.y, t)) < 1.2) {
            v *= 0.01;
        }

        // Prepare for chromatic Abbreveation
        vec2 focus = vec2(0.5);
        float d = v * 0.6;
        vec2 ruv = focus + (uv - focus) * (1. - d);
        vec2 guv = focus + (uv - focus) * (1. - 2. * d);
        vec2 buv = focus + (uv - focus) * (1. - 3. * d);

        // Random Glitch
        if (v > 0.1) {
            // Randomize y
            float y = floor(uv.y * 13. * sin(35. * t)) + 1.;
            if (sin(36. * y * v) > 0.9) {
                ruv.x = uv.x + sin(76. * y) * 0.1;
                guv.x = uv.x + sin(34. * y) * 0.1;
                buv.x = uv.x + sin(59. * y) * 0.1;
            }

            // RGB Shift
            v = pow(v * 1.5, 2.) * 0.15;
            color.rgb *= 0.3;
            color.r += readTex(src, vec2(uv.x + sin(t * 123.45) * v, uv.y)).r;
            color.g += readTex(src, vec2(uv.x + sin(t * 157.67) * v, uv.y)).g;
            color.b += readTex(src, vec2(uv.x + sin(t * 143.67) * v, uv.y)).b;
        }

        // Compose Chromatic Abbreveation
        if (abs(nn(uv.y, t)) > 1.1) {
            color.r = color.r * 0.5 + color.r * texture(src, ruv).r;
            color.g = color.g * 0.5 + color.g * texture(src, guv).g;
            color.b = color.b * 0.5 + color.b * texture(src, buv).b;
            color *= 2.;
        }

        outColor = color;
        outColor.a = smoothstep(0.0, 0.8, max(color.r, max(color.g, color.b)));
    }
    `,
    pixelate: `
    ${COMMON_HEADER}
    ${READ_TEX}

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;

        float b = sin(time * 2.) * 32. + 48.;
        uv = floor(uv * b) / b;
        outColor = readTex(src, uv);
    }
    `,
    rgbGlitch: `
    ${COMMON_HEADER}
    ${READ_TEX}

    float random(vec2 st) {
        return fract(sin(dot(st, vec2(948.,824.))) * 30284.);
    }

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        vec2 uvr = uv, uvg = uv, uvb = uv;

        float tt = mod(time, 17.);

        if (fract(tt * 0.73) > .8 || fract(tt * 0.91) > .8) {
            float t = floor(tt * 11.);

            float n = random(vec2(t, floor(uv.y * 17.7)));
            if (n > .7) {
                uvr.x += random(vec2(t, 1.)) * .1 - 0.05;
                uvg.x += random(vec2(t, 2.)) * .1 - 0.05;
                uvb.x += random(vec2(t, 3.)) * .1 - 0.05;
            }

            float ny = random(vec2(t * 17. + floor(uv * 19.7)));
            if (ny > .7) {
                uvr.x += random(vec2(t, 4.)) * .1 - 0.05;
                uvg.x += random(vec2(t, 5.)) * .1 - 0.05;
                uvb.x += random(vec2(t, 6.)) * .1 - 0.05;
            }
        }

        vec4 cr = readTex(src, uvr);
        vec4 cg = readTex(src, uvg);
        vec4 cb = readTex(src, uvb);

        outColor = vec4(
            cr.r,
            cg.g,
            cb.b,
            step(.1, cr.a + cg.a + cb.a)
        );
    }
    `,
    rgbShift: `
    ${COMMON_HEADER}
    ${READ_TEX}

    float nn(float y, float t) {
        float n = (
            sin(y * .07 + t * 8. + sin(y * .5 + t * 10.)) +
            sin(y * .7 + t * 2. + sin(y * .3 + t * 8.)) * .7 +
            sin(y * 1.1 + t * 2.8) * .4
        );

        n += sin(y * 124. + t * 100.7) * sin(y * 877. - t * 38.8) * .3;

        return n;
    }

    float step2(float t, vec2 uv) {
        return step(t, uv.x) * step(t, uv.y);
    }

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        vec2 uvr = uv, uvg = uv, uvb = uv;

        float t = mod(time, 30.);

        float amp = 10. / resolution.x;

        if (abs(nn(uv.y, t)) > 1.) {
            uvr.x += nn(uv.y, t) * amp;
            uvg.x += nn(uv.y, t + 10.) * amp;
            uvb.x += nn(uv.y, t + 20.) * amp;
        }

        vec4 cr = readTex(src, uvr);
        vec4 cg = readTex(src, uvg);
        vec4 cb = readTex(src, uvb);

        outColor = vec4(
            cr.r,
            cg.g,
            cb.b,
            smoothstep(.0, 1., cr.a + cg.a + cb.a)
        );
    }
    `,
    halftone: `
    // Halftone Effect by zoidberg
    // https://www.interactiveshaderformat.com/sketches/234

    ${COMMON_HEADER}
    ${READ_TEX}

    // TODO: uniform
    #define gridSize 10.0
    #define dotSize 0.7
    #define smoothing 0.15
    #define speed 1.0

    #define IMG_PIXEL(x, y) readTex(x, (y - offset) / resolution);

    vec4 gridRot = vec4(15.0, 45.0, 75.0, 0.0);

    // during calculation we find the closest dot to a frag, determine its size, and then determine the size of the four dots above/below/right/left of it. this array of offsets move "one left", "one up", "one right", and "one down"...
    vec2 originOffsets[4];

    void main() {
        vec2 fragCoord = gl_FragCoord.xy - offset;

        // a halftone is an overlapping series of grids of dots
        // each grid of dots is rotated by a different amount
        // the size of the dots determines the colors. the shape of the dot should never change (always be a dot with regular edges)
        originOffsets[0] = vec2(-1.0, 0.0);
        originOffsets[1] = vec2(0.0, 1.0);
        originOffsets[2] = vec2(1.0, 0.0);
        originOffsets[3] = vec2(0.0, -1.0);

        vec3 rgbAmounts = vec3(0.0);

        // for each of the channels (i) of RGB...
        for (float i=0.0; i<3.0; ++i) {
            // figure out the rotation of the grid in radians
            float rotRad = radians(gridRot[int(i)]);

            // the grids are rotated counter-clockwise- to find the nearest dot, take the fragment pixel loc,
            // rotate it clockwise, and split by the grid to find the center of the dot. then rotate this
            // coord counter-clockwise to yield the location of the center of the dot in pixel coords local to the render space
            mat2 ccTrans = mat2(vec2(cos(rotRad), sin(rotRad)), vec2(-1.0*sin(rotRad), cos(rotRad)));
            mat2 cTrans = mat2(vec2(cos(rotRad), -1.0*sin(rotRad)), vec2(sin(rotRad), cos(rotRad)));

            // find the location of the frag in the grid (prior to rotating it)
            vec2 gridFragLoc = cTrans * fragCoord.xy;

            // find the center of the dot closest to the frag- there's no "round" in GLSL 1.2, so do a "floor" to find the dot to the bottom-left of the frag, then figure out if the frag would be in the top and right halves of that square to find the closest dot to the frag
            vec2 gridOriginLoc = vec2(floor(gridFragLoc.x/gridSize), floor(gridFragLoc.y/gridSize));

            vec2 tmpGridCoords = gridFragLoc/vec2(gridSize);
            bool fragAtTopOfGrid = ((tmpGridCoords.y-floor(tmpGridCoords.y)) > (gridSize/2.0)) ? true : false;
            bool fragAtRightOfGrid = ((tmpGridCoords.x-floor(tmpGridCoords.x)) > (gridSize/2.0)) ? true : false;
            if (fragAtTopOfGrid)
                gridOriginLoc.y = gridOriginLoc.y + 1.0;
            if (fragAtRightOfGrid)
                gridOriginLoc.x = gridOriginLoc.x + 1.0;

            // ...at this point, "gridOriginLoc" contains the grid coords of the nearest dot to the fragment being rendered
            // convert the location of the center of the dot from grid coords to pixel coords
            vec2 gridDotLoc = vec2(gridOriginLoc.x*gridSize, gridOriginLoc.y*gridSize) + vec2(gridSize/2.0);

            // rotate the pixel coords of the center of the dot so they become relative to the rendering space
            vec2 renderDotLoc = ccTrans * gridDotLoc;

            // get the color of the pixel of the input image under this dot (the color will ultimately determine the size of the dot)
            vec4 renderDotImageColorRGB = IMG_PIXEL(src, renderDotLoc + offset);

            // the amount of this channel is taken from the same channel of the color of the pixel of the input image under this halftone dot
            float imageChannelAmount = renderDotImageColorRGB[int(i)];

            // the size of the dot is determined by the value of the channel
            float dotRadius = imageChannelAmount * (gridSize * dotSize);
            float fragDistanceToDotCenter = distance(fragCoord.xy, renderDotLoc);
            if (fragDistanceToDotCenter < dotRadius) {
                rgbAmounts[int(i)] += smoothstep(dotRadius, dotRadius-(dotRadius*smoothing), fragDistanceToDotCenter);
            }

            // calcluate the size of the dots abov/below/to the left/right to see if they're overlapping
            for (float j=0.0; j<4.0; ++j) {
                gridDotLoc = vec2((gridOriginLoc.x+originOffsets[int(j)].x)*gridSize, (gridOriginLoc.y+originOffsets[int(j)].y)*gridSize) + vec2(gridSize/2.0);

                renderDotLoc = ccTrans * gridDotLoc;
                renderDotImageColorRGB = IMG_PIXEL(src, renderDotLoc + offset);

                imageChannelAmount = renderDotImageColorRGB[int(i)];
                dotRadius = imageChannelAmount * (gridSize*1.50/2.0);
                fragDistanceToDotCenter = distance(fragCoord.xy, renderDotLoc);
                if (fragDistanceToDotCenter < dotRadius) {
                    rgbAmounts[int(i)] += smoothstep(dotRadius, dotRadius-(dotRadius*smoothing), fragDistanceToDotCenter);
                }
            }
        }

        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        vec4 original = readTex(src, uv);
        float alpha = step(.1, rgbAmounts[0] + rgbAmounts[1] + rgbAmounts[2] + original.a);

        outColor = vec4(rgbAmounts[0], rgbAmounts[1], rgbAmounts[2], alpha);
    }
    `,
    sinewave: `
    ${COMMON_HEADER}
    ${READ_TEX}

    vec4 draw(vec2 uv) {
        vec2 uvr = uv, uvg = uv, uvb = uv;

        float amp = 20. / resolution.x;

        uvr.x += sin(uv.y * 7. + time * 3.) * amp;
        uvg.x += sin(uv.y * 7. + time * 3. + .4) * amp;
        uvb.x += sin(uv.y * 7. + time * 3. + .8) * amp;

        vec4 cr = readTex(src, uvr);
        vec4 cg = readTex(src, uvg);
        vec4 cb = readTex(src, uvb);

        return vec4(
            cr.r,
            cg.g,
            cb.b,
            cr.a + cg.a + cb.a
        );
    }

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;

        // x blur
        vec2 dx = vec2(2, 0) / resolution.x;
        outColor = (draw(uv) * 2. + draw(uv + dx) + draw(uv - dx)) / 4.;
    }
    `,
    shine: `
    ${COMMON_HEADER}
    ${READ_TEX}

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;

        vec2 p = uv * 2. - 1.;
        float a = atan(p.y, p.x);

        vec4 col = readTex(src, uv);
        float gray = length(col.rgb);

        float level = 1. + sin(a * 10. + time * 3.) * 0.2;

        outColor = vec4(1, 1, .5, col.a) * level;
    }
    `,
    blink: `
    ${COMMON_HEADER}
    ${READ_TEX}

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;

        outColor = readTex(src, uv) * (sin(time * 5.) * 0.2 + 0.8);
    }

    `,
    spring: `
    ${COMMON_HEADER}
    ${READ_TEX}

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        uv = (uv - .5) * (1.05 + sin(time * 5.) * 0.05) + .5;
        outColor = readTex(src, uv);
    }
    `,
    duotone: `
    ${COMMON_HEADER}
    ${READ_TEX}

    uniform vec4 color1;
    uniform vec4 color2;
    uniform float speed;

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        vec4 color = readTex(src, uv);

        float gray = dot(color.rgb, vec3(0.2, 0.7, 0.08));
        float t = mod(gray * 2.0 + time * speed, 2.0);

        if (t < 1.) {
            outColor = mix(color1, color2, fract(t));
        } else {
            outColor = mix(color2, color1, fract(t));
        }

        outColor.a *= color.a;
    }
    `,
    tritone: `
    ${COMMON_HEADER}
    ${READ_TEX}

    uniform vec4 color1;
    uniform vec4 color2;
    uniform vec4 color3;
    uniform float speed;

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        vec4 color = readTex(src, uv);

        float gray = dot(color.rgb, vec3(0.2, 0.7, 0.08));
        float t = mod(gray * 3.0 + time * speed, 3.0);

        if (t < 1.) {
            outColor = mix(color1, color2, fract(t));
        } else if (t < 2.) {
            outColor = mix(color2, color3, fract(t));
        } else {
            outColor = mix(color3, color1, fract(t));
        }

        outColor.a *= color.a;
    }
    `,
    hueShift: `
    ${COMMON_HEADER}
    ${READ_TEX}

    uniform float shift;

    vec3 hsv2rgb(vec3 c) {
        vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
        vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
        return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
    }

    vec3 rgb2hsv(vec3 c) {
        vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
        vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
        vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

        float d = q.x - min(q.w, q.y);
        float e = 1.0e-10;
        return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
    }

    vec3 hueShift(vec3 rgb, float t) {
        vec3 hsv = rgb2hsv(rgb);
        hsv.x = fract(hsv.x + t);
        return hsv2rgb(hsv);
    }

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        vec4 color = readTex(src, uv);
        color.rgb = hueShift(color.rgb, shift);
        outColor = color;
    }
    `,
    warpTransition: `
    ${COMMON_HEADER}
    uniform float enterTime;
    uniform float leaveTime;

    ${READ_TEX}

    #define DURATION 1.0

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;

        float t1 = enterTime / DURATION;
        float t2 = leaveTime / DURATION;
        float t = clamp(min(t1, 1. - t2), 0., 1.);

        if (t == 0.) {
            discard;
        }

        if (t < 1.) {
            uv.x += sin(floor(uv.y * 300.)) * 3. * exp(t * -10.);
        }

        outColor = readTex(src, uv);
    }
    `,
    slitScanTransition: `
    ${COMMON_HEADER}
    ${READ_TEX}

    uniform float enterTime;
    uniform float leaveTime;

    #define DURATION 1.0

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;

        float t1 = enterTime / DURATION;
        float t2 = leaveTime / DURATION;

        // Do not render before enter or after leave
        if (t1 < 0. || 1. < t2) {
            discard;
        }

        if (0. < t2) {
            // Leaving
            float t = 1. - t2;
            uv.y = uv.y < t ? uv.y : t;
        } else if (t1 < 1.) {
            // Entering
            float t = 1. - t1;
            uv.y = uv.y < t ? t : uv.y;
        }

        outColor = readTex(src, uv);
    }
    `,
    pixelateTransition: `
    ${COMMON_HEADER}
    ${READ_TEX}

    uniform float enterTime;
    uniform float leaveTime;

    #define DURATION 1.0

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;

        float t1 = enterTime / DURATION;
        float t2 = leaveTime / DURATION;
        float t = clamp(min(t1, 1. - t2), 0., 1.);

        if (t == 0.) {
            discard;
        } else if (t < 1.) {
            float b = floor(t * 64.);
            uv = (floor(uv * b) + .5) / b;
        }

        outColor = readTex(src, uv);
    }
    `,
    focusTransition: `
    ${COMMON_HEADER}
    ${READ_TEX}

    uniform float intersection;

    void main (void) {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        float t = smoothstep(0., 1., intersection);

        outColor = mix(
            readTex(src, uv + vec2(1. - t, 0)),
            readTex(src, uv + vec2(-(1. - t), 0)),
            0.5
        ) * intersection;
    }
    `,
    invert: `
    ${COMMON_HEADER}
    ${READ_TEX}

    void main() {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        vec4 color = readTex(src, uv);
        outColor = vec4(1.0 - color.rgb, color.a);
    }
    `,
    grayscale: `
    ${COMMON_HEADER}
    ${READ_TEX}

    void main() {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        vec4 color = readTex(src, uv);
        float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
        outColor = vec4(vec3(gray), color.a);
    }
    `,
    vignette: `
    ${COMMON_HEADER}
    ${READ_TEX}

    uniform float intensity;
    uniform float radius;
    uniform float power;

    void main() {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;
        outColor = readTex(src, uv);

        vec2 p = uv * 2.0 - 1.0;
        p.x *= resolution.x / resolution.y;

        float l = max(length(p) - radius, 0.);
        outColor *= 1. - pow(l, power) * intensity;
    }
    `,
    chromatic: `
    ${COMMON_HEADER}
    ${READ_TEX}

    uniform float intensity;
    uniform float radius;
    uniform float power;


    vec4 mirrorTex(sampler2D tex, vec2 uv) {
        vec2 uv2 = 1. - abs(1. - mod(uv, 2.0));
        return texture(tex, uv2);
    }

    void main() {
        vec2 uv = (gl_FragCoord.xy - offset) / resolution;

        vec2 p = uv * 2.0 - 1.0;
        p.x *= resolution.x / resolution.y;

        float l = max(length(p) - radius, 0.);
        float d = pow(l, power) * (intensity * 0.1);

        vec2 uvR = (uv - .5) / (1.0 + d * 1.) + 0.5;
        vec2 uvG = (uv - .5) / (1.0 + d * 2.) + 0.5;
        vec2 uvB = (uv - .5) / (1.0 + d * 3.) + 0.5;

        vec4 cr = mirrorTex(src, uvR);
        vec4 cg = mirrorTex(src, uvG);
        vec4 cb = mirrorTex(src, uvB);

        outColor = vec4(cr.r, cg.g, cb.b, (cr.a + cg.a + cb.a) / 3.0);
    }
    `
  };

  // node_modules/@vfx-js/core/lib/esm/html-in-canvas.js
  function isCrossOrigin(img) {
    if (!img.src || img.src.startsWith("data:")) {
      return false;
    }
    try {
      const imgUrl = new URL(img.src, location.href);
      return imgUrl.origin !== location.origin;
    } catch (e) {
      return false;
    }
  }
  async function toBlobUrl(url) {
    const res = await fetch(url);
    const blob = await res.blob();
    return URL.createObjectURL(blob);
  }
  async function inlineCrossOriginImages(root) {
    const imgs = Array.from(root.querySelectorAll("img"));
    const crossOriginImgs = imgs.filter((img) => img.complete && img.naturalWidth > 0 && isCrossOrigin(img));
    if (crossOriginImgs.length === 0) {
      return () => {
      };
    }
    const originals = /* @__PURE__ */ new Map();
    const blobUrls = [];
    await Promise.all(crossOriginImgs.map(async (img) => {
      try {
        const blobUrl = await toBlobUrl(img.src);
        originals.set(img, img.src);
        blobUrls.push(blobUrl);
        await new Promise((resolve) => {
          img.addEventListener("load", () => resolve(), {
            once: true
          });
          img.src = blobUrl;
        });
      } catch (e) {
      }
    }));
    return () => {
      for (const [img, src] of originals) {
        img.src = src;
      }
      for (const url of blobUrls) {
        URL.revokeObjectURL(url);
      }
    };
  }
  var MARGIN_PROPS = [
    "margin-top",
    "margin-right",
    "margin-bottom",
    "margin-left"
  ];
  var POSITION_FLOW_STYLES = [
    "position",
    "top",
    "right",
    "bottom",
    "left",
    "float",
    "flex",
    "flex-grow",
    "flex-shrink",
    "flex-basis",
    "align-self",
    "justify-self",
    "place-self",
    "order",
    "grid-column",
    "grid-column-start",
    "grid-column-end",
    "grid-row",
    "grid-row-start",
    "grid-row-end",
    "grid-area"
  ];
  var canvasResizeObservers = /* @__PURE__ */ new WeakMap();
  var childResizeObservers = /* @__PURE__ */ new WeakMap();
  var savedMargins = /* @__PURE__ */ new WeakMap();
  var savedWidths = /* @__PURE__ */ new WeakMap();
  var savedBoxSizing = /* @__PURE__ */ new WeakMap();
  var imageRestorers = /* @__PURE__ */ new WeakMap();
  async function setupCapture(canvas, opts) {
    const ctx = canvas.getContext("2d");
    if (!ctx) {
      throw new Error("Failed to get 2d context from layoutsubtree canvas");
    }
    const { onCapture, maxSize } = opts;
    let offscreen = null;
    let resolveFirst = null;
    const firstCapture = new Promise((resolve) => {
      resolveFirst = resolve;
    });
    canvas.onpaint = () => {
      const child2 = canvas.firstElementChild;
      if (!child2 || canvas.width === 0 || canvas.height === 0) {
        return;
      }
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawElementImage(child2, 0, 0);
      let w = canvas.width;
      let h = canvas.height;
      if (maxSize && (w > maxSize || h > maxSize)) {
        const s = Math.min(maxSize / w, maxSize / h);
        w = Math.floor(w * s);
        h = Math.floor(h * s);
      }
      if (!offscreen || offscreen.width !== w || offscreen.height !== h) {
        offscreen = new OffscreenCanvas(w, h);
      }
      const offCtx = offscreen.getContext("2d");
      if (!offCtx) {
        return;
      }
      offCtx.clearRect(0, 0, w, h);
      offCtx.drawImage(canvas, 0, 0, w, h);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      if (resolveFirst) {
        resolveFirst(offscreen);
        resolveFirst = null;
        return;
      }
      onCapture(offscreen);
    };
    const canvasRO = new ResizeObserver((entries) => {
      var _a, _b;
      for (const entry of entries) {
        const dpSize = (_a = entry.devicePixelContentBoxSize) == null ? void 0 : _a[0];
        if (dpSize) {
          canvas.width = dpSize.inlineSize;
          canvas.height = dpSize.blockSize;
        } else {
          const box = (_b = entry.borderBoxSize) == null ? void 0 : _b[0];
          if (box) {
            const dpr = window.devicePixelRatio;
            canvas.width = Math.round(box.inlineSize * dpr);
            canvas.height = Math.round(box.blockSize * dpr);
          }
        }
      }
      canvas.requestPaint();
    });
    canvasRO.observe(canvas, { box: "device-pixel-content-box" });
    canvasResizeObservers.set(canvas, canvasRO);
    const child = canvas.firstElementChild;
    let lastChildHeight = "";
    if (child) {
      const childRO = new ResizeObserver((entries) => {
        var _a;
        const box = (_a = entries[0].borderBoxSize) == null ? void 0 : _a[0];
        if (!box) {
          return;
        }
        const h = `${Math.round(box.blockSize)}px`;
        if (h !== lastChildHeight) {
          lastChildHeight = h;
          canvas.style.setProperty("height", h);
        }
      });
      childRO.observe(child);
      childResizeObservers.set(canvas, childRO);
    }
    return firstCapture;
  }
  function teardownCapture(canvas) {
    canvas.onpaint = null;
    const canvasRO = canvasResizeObservers.get(canvas);
    if (canvasRO) {
      canvasRO.disconnect();
      canvasResizeObservers.delete(canvas);
    }
    const childRO = childResizeObservers.get(canvas);
    if (childRO) {
      childRO.disconnect();
      childResizeObservers.delete(canvas);
    }
  }
  async function wrapElement(element, opts) {
    var _a;
    const rect = element.getBoundingClientRect();
    const canvas = document.createElement("canvas");
    canvas.setAttribute("layoutsubtree", "");
    canvas.className = element.className;
    const styleAttr = element.getAttribute("style");
    if (styleAttr) {
      canvas.setAttribute("style", styleAttr);
    }
    canvas.style.setProperty("padding", "0");
    canvas.style.setProperty("border", "none");
    canvas.style.setProperty("box-sizing", "content-box");
    canvas.style.setProperty("background", "transparent");
    const cs = getComputedStyle(element);
    const display = cs.display === "inline" ? "block" : cs.display;
    canvas.style.setProperty("display", display);
    for (const prop of MARGIN_PROPS) {
      canvas.style.setProperty(prop, cs.getPropertyValue(prop));
    }
    for (const prop of POSITION_FLOW_STYLES) {
      canvas.style.setProperty(prop, cs.getPropertyValue(prop));
    }
    if (element.style.width.endsWith("px")) {
      canvas.style.setProperty("width", `${rect.width}px`);
    } else {
      canvas.style.setProperty("width", "100%");
    }
    if (!canvas.style.height) {
      canvas.style.setProperty("height", `${rect.height}px`);
    }
    const dpr = window.devicePixelRatio;
    canvas.width = Math.round(rect.width * dpr);
    canvas.height = Math.round(rect.height * dpr);
    savedMargins.set(element, element.style.margin);
    savedWidths.set(element, element.style.width);
    savedBoxSizing.set(element, element.style.boxSizing);
    (_a = element.parentNode) == null ? void 0 : _a.insertBefore(canvas, element);
    canvas.appendChild(element);
    element.style.setProperty("margin", "0");
    element.style.setProperty("width", "100%");
    element.style.setProperty("box-sizing", "border-box");
    const restore = await inlineCrossOriginImages(element);
    imageRestorers.set(canvas, restore);
    const initialCapture = await setupCapture(canvas, opts);
    return { canvas, initialCapture };
  }
  function unwrapElement(canvas, element) {
    var _a;
    teardownCapture(canvas);
    const restoreImages = imageRestorers.get(canvas);
    if (restoreImages) {
      restoreImages();
      imageRestorers.delete(canvas);
    }
    (_a = canvas.parentNode) == null ? void 0 : _a.insertBefore(element, canvas);
    canvas.remove();
    const savedMargin = savedMargins.get(element);
    if (savedMargin !== void 0) {
      element.style.margin = savedMargin;
      savedMargins.delete(element);
    }
    const savedWidth = savedWidths.get(element);
    if (savedWidth !== void 0) {
      element.style.width = savedWidth;
      savedWidths.delete(element);
    }
    const savedBS = savedBoxSizing.get(element);
    if (savedBS !== void 0) {
      element.style.boxSizing = savedBS;
      savedBoxSizing.delete(element);
    }
  }

  // node_modules/@vfx-js/core/lib/esm/html-in-canvas-support.js
  var supported;
  function supportsHtmlInCanvas() {
    if (supported !== void 0) {
      return supported;
    }
    try {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      supported = ctx !== null && typeof ctx.drawElementImage === "function" && typeof canvas.requestPaint === "function";
    } catch (e) {
      supported = false;
    }
    return supported;
  }

  // node_modules/@vfx-js/core/lib/esm/types.js
  function getVFXOpts(opts) {
    var _a, _b, _c, _d, _e;
    const defaultPixelRatio = typeof window !== "undefined" ? window.devicePixelRatio : 1;
    let scrollPadding;
    if (opts.scrollPadding === void 0) {
      scrollPadding = [0.1, 0.1];
    } else if (opts.scrollPadding === false) {
      scrollPadding = [0, 0];
    } else if (Array.isArray(opts.scrollPadding)) {
      scrollPadding = [
        (_a = opts.scrollPadding[0]) != null ? _a : 0.1,
        (_b = opts.scrollPadding[1]) != null ? _b : 0.1
      ];
    } else {
      scrollPadding = [opts.scrollPadding, opts.scrollPadding];
    }
    let postEffects;
    if (opts.postEffect === void 0) {
      postEffects = [];
    } else if (Array.isArray(opts.postEffect)) {
      postEffects = opts.postEffect;
    } else {
      postEffects = [opts.postEffect];
    }
    return {
      pixelRatio: (_c = opts.pixelRatio) != null ? _c : defaultPixelRatio,
      zIndex: (_d = opts.zIndex) != null ? _d : void 0,
      autoplay: (_e = opts.autoplay) != null ? _e : true,
      fixedCanvas: opts.scrollPadding === false,
      scrollPadding,
      wrapper: opts.wrapper,
      postEffects
    };
  }

  // node_modules/@vfx-js/core/lib/esm/gl/texture.js
  var __classPrivateFieldSet = function(receiver, state2, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state2.set(receiver, value), value;
  };
  var __classPrivateFieldGet = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _Texture_instances;
  var _Texture_ctx;
  var _Texture_uploaded;
  var _Texture_registered;
  var _Texture_external;
  var _Texture_create;
  var _Texture_upload;
  var _Texture_applyParams;
  var Texture = class {
    constructor(ctx, source, opts) {
      _Texture_instances.add(this);
      this.wrapS = "clamp";
      this.wrapT = "clamp";
      this.minFilter = "linear";
      this.magFilter = "linear";
      this.needsUpdate = true;
      this.source = null;
      _Texture_ctx.set(this, void 0);
      _Texture_uploaded.set(this, false);
      _Texture_registered.set(this, void 0);
      _Texture_external.set(this, void 0);
      __classPrivateFieldSet(this, _Texture_ctx, ctx, "f");
      this.gl = ctx.gl;
      const external = opts == null ? void 0 : opts.externalHandle;
      __classPrivateFieldSet(this, _Texture_external, external !== void 0, "f");
      if (external !== void 0) {
        this.texture = external;
        __classPrivateFieldSet(this, _Texture_uploaded, true, "f");
        this.needsUpdate = false;
      } else {
        __classPrivateFieldGet(this, _Texture_instances, "m", _Texture_create).call(this);
      }
      if (source) {
        this.source = source;
      }
      __classPrivateFieldSet(this, _Texture_registered, (opts == null ? void 0 : opts.autoRegister) !== false && !__classPrivateFieldGet(this, _Texture_external, "f"), "f");
      if (__classPrivateFieldGet(this, _Texture_registered, "f")) {
        ctx.addResource(this);
      }
    }
    restore() {
      if (__classPrivateFieldGet(this, _Texture_external, "f")) {
        return;
      }
      __classPrivateFieldGet(this, _Texture_instances, "m", _Texture_create).call(this);
      __classPrivateFieldSet(this, _Texture_uploaded, false, "f");
      this.needsUpdate = true;
    }
    bind(unit) {
      const gl = this.gl;
      gl.activeTexture(gl.TEXTURE0 + unit);
      gl.bindTexture(gl.TEXTURE_2D, this.texture);
      if (this.needsUpdate) {
        __classPrivateFieldGet(this, _Texture_instances, "m", _Texture_upload).call(this);
        this.needsUpdate = false;
      }
    }
    dispose() {
      if (__classPrivateFieldGet(this, _Texture_registered, "f")) {
        __classPrivateFieldGet(this, _Texture_ctx, "f").removeResource(this);
      }
      if (!__classPrivateFieldGet(this, _Texture_external, "f")) {
        this.gl.deleteTexture(this.texture);
      }
    }
  };
  _Texture_ctx = /* @__PURE__ */ new WeakMap(), _Texture_uploaded = /* @__PURE__ */ new WeakMap(), _Texture_registered = /* @__PURE__ */ new WeakMap(), _Texture_external = /* @__PURE__ */ new WeakMap(), _Texture_instances = /* @__PURE__ */ new WeakSet(), _Texture_create = function _Texture_create2() {
    const tex = this.gl.createTexture();
    if (!tex) {
      throw new Error("[VFX-JS] Failed to create texture");
    }
    this.texture = tex;
  }, _Texture_upload = function _Texture_upload2() {
    const gl = this.gl;
    const src = this.source;
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false);
    gl.pixelStorei(gl.UNPACK_ALIGNMENT, 4);
    if (src) {
      try {
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, src);
      } catch (e) {
        console.error(e);
      }
    } else if (!__classPrivateFieldGet(this, _Texture_uploaded, "f")) {
      const pixel = new Uint8Array([0, 0, 0, 0]);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, pixel);
    }
    __classPrivateFieldGet(this, _Texture_instances, "m", _Texture_applyParams).call(this);
    __classPrivateFieldSet(this, _Texture_uploaded, true, "f");
  }, _Texture_applyParams = function _Texture_applyParams2() {
    const gl = this.gl;
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, wrapEnum(gl, this.wrapS));
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, wrapEnum(gl, this.wrapT));
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, filterEnum(gl, this.minFilter));
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, filterEnum(gl, this.magFilter));
  };
  function wrapEnum(gl, w) {
    if (w === "repeat") {
      return gl.REPEAT;
    }
    if (w === "mirror") {
      return gl.MIRRORED_REPEAT;
    }
    return gl.CLAMP_TO_EDGE;
  }
  function filterEnum(gl, f) {
    return f === "nearest" ? gl.NEAREST : gl.LINEAR;
  }
  function loadImage(url) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = "anonymous";
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = url;
    });
  }

  // node_modules/@vfx-js/core/lib/esm/gl/framebuffer.js
  var __classPrivateFieldSet2 = function(receiver, state2, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state2.set(receiver, value), value;
  };
  var __classPrivateFieldGet2 = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _Framebuffer_instances;
  var _Framebuffer_ctx;
  var _Framebuffer_allocate;
  var Framebuffer = class {
    constructor(ctx, width, height, opts = {}) {
      var _a, _b;
      _Framebuffer_instances.add(this);
      _Framebuffer_ctx.set(this, void 0);
      __classPrivateFieldSet2(this, _Framebuffer_ctx, ctx, "f");
      this.gl = ctx.gl;
      this.width = Math.max(1, Math.floor(width));
      this.height = Math.max(1, Math.floor(height));
      this.float = (_a = opts.float) != null ? _a : false;
      this.mipmap = (_b = opts.mipmap) != null ? _b : false;
      this.texture = new Texture(ctx, void 0, { autoRegister: false });
      const w = opts.wrap;
      if (w !== void 0) {
        if (typeof w === "string") {
          this.texture.wrapS = w;
          this.texture.wrapT = w;
        } else {
          this.texture.wrapS = w[0];
          this.texture.wrapT = w[1];
        }
      }
      if (opts.filter !== void 0) {
        this.texture.minFilter = opts.filter;
        this.texture.magFilter = opts.filter;
      }
      __classPrivateFieldGet2(this, _Framebuffer_instances, "m", _Framebuffer_allocate).call(this);
      ctx.addResource(this);
    }
    setSize(width, height) {
      const w = Math.max(1, Math.floor(width));
      const h = Math.max(1, Math.floor(height));
      if (w === this.width && h === this.height) {
        return;
      }
      this.width = w;
      this.height = h;
      __classPrivateFieldGet2(this, _Framebuffer_instances, "m", _Framebuffer_allocate).call(this);
    }
    restore() {
      this.texture.restore();
      __classPrivateFieldGet2(this, _Framebuffer_instances, "m", _Framebuffer_allocate).call(this);
    }
    dispose() {
      __classPrivateFieldGet2(this, _Framebuffer_ctx, "f").removeResource(this);
      this.gl.deleteFramebuffer(this.fbo);
      this.texture.dispose();
    }
    /**
     * Regenerate mips from level 0. No-op when this FB was not created
     * with `mipmap: true`.
     */
    generateMipmaps() {
      if (!this.mipmap) {
        return;
      }
      const gl = this.gl;
      gl.bindTexture(gl.TEXTURE_2D, this.texture.texture);
      gl.generateMipmap(gl.TEXTURE_2D);
      gl.bindTexture(gl.TEXTURE_2D, null);
    }
  };
  _Framebuffer_ctx = /* @__PURE__ */ new WeakMap(), _Framebuffer_instances = /* @__PURE__ */ new WeakSet(), _Framebuffer_allocate = function _Framebuffer_allocate2() {
    const gl = this.gl;
    const oldFbo = this.fbo;
    const fbo = gl.createFramebuffer();
    if (!fbo) {
      throw new Error("[VFX-JS] Failed to create framebuffer");
    }
    this.fbo = fbo;
    const tex = this.texture.texture;
    gl.bindTexture(gl.TEXTURE_2D, tex);
    const floatLinear = __classPrivateFieldGet2(this, _Framebuffer_ctx, "f").floatLinearFilter;
    const internalFormat = this.float ? floatLinear ? gl.RGBA32F : gl.RGBA16F : gl.RGBA8;
    const type = this.float ? floatLinear ? gl.FLOAT : gl.HALF_FLOAT : gl.UNSIGNED_BYTE;
    if (this.mipmap) {
      const levels = Math.floor(Math.log2(Math.max(this.width, this.height))) + 1;
      let w = this.width;
      let h = this.height;
      for (let level = 0; level < levels; level++) {
        gl.texImage2D(gl.TEXTURE_2D, level, internalFormat, w, h, 0, gl.RGBA, type, null);
        w = Math.max(1, w >> 1);
        h = Math.max(1, h >> 1);
      }
    } else {
      gl.texImage2D(gl.TEXTURE_2D, 0, internalFormat, this.width, this.height, 0, gl.RGBA, type, null);
    }
    const baseMin = this.texture.minFilter === "nearest" ? gl.NEAREST : gl.LINEAR;
    const magF = this.texture.magFilter === "nearest" ? gl.NEAREST : gl.LINEAR;
    const minF = this.mipmap ? this.texture.minFilter === "nearest" ? gl.NEAREST_MIPMAP_NEAREST : gl.LINEAR_MIPMAP_LINEAR : baseMin;
    const wrapS = wrapEnum2(gl, this.texture.wrapS);
    const wrapT = wrapEnum2(gl, this.texture.wrapT);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, minF);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, magF);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, wrapS);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, wrapT);
    gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tex, 0);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    gl.bindTexture(gl.TEXTURE_2D, null);
    this.texture.needsUpdate = false;
    this.texture.source = null;
    if (oldFbo) {
      gl.deleteFramebuffer(oldFbo);
    }
  };
  function wrapEnum2(gl, w) {
    if (w === "repeat") {
      return gl.REPEAT;
    }
    if (w === "mirror") {
      return gl.MIRRORED_REPEAT;
    }
    return gl.CLAMP_TO_EDGE;
  }

  // node_modules/@vfx-js/core/lib/esm/gl-rect.js
  function rectToGLRect(rect, containerHeight, paddingX, paddingY) {
    return {
      x: rect.left + paddingX,
      y: containerHeight - paddingY - rect.bottom,
      w: rect.right - rect.left,
      h: rect.bottom - rect.top
    };
  }
  function getGLRect(x, y, w, h) {
    return { x, y, w, h };
  }

  // node_modules/@vfx-js/core/lib/esm/backbuffer.js
  var __classPrivateFieldSet3 = function(receiver, state2, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state2.set(receiver, value), value;
  };
  var __classPrivateFieldGet3 = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _Backbuffer_width;
  var _Backbuffer_height;
  var _Backbuffer_pixelRatio;
  var _Backbuffer_buffers;
  var Backbuffer = class {
    constructor(ctx, width, height, pixelRatio, float, opts = {}) {
      _Backbuffer_width.set(this, void 0);
      _Backbuffer_height.set(this, void 0);
      _Backbuffer_pixelRatio.set(this, void 0);
      _Backbuffer_buffers.set(this, void 0);
      __classPrivateFieldSet3(this, _Backbuffer_width, width, "f");
      __classPrivateFieldSet3(this, _Backbuffer_height, height, "f");
      __classPrivateFieldSet3(this, _Backbuffer_pixelRatio, pixelRatio, "f");
      const pwidth = width * pixelRatio;
      const pheight = height * pixelRatio;
      const fbOpts = {
        float,
        wrap: opts.wrap,
        filter: opts.filter,
        mipmap: opts.mipmap
      };
      __classPrivateFieldSet3(this, _Backbuffer_buffers, [
        new Framebuffer(ctx, pwidth, pheight, fbOpts),
        new Framebuffer(ctx, pwidth, pheight, fbOpts)
      ], "f");
    }
    /** Read texture (the previous frame's output). */
    get texture() {
      return __classPrivateFieldGet3(this, _Backbuffer_buffers, "f")[0].texture;
    }
    /** Write target for the current frame. */
    get target() {
      return __classPrivateFieldGet3(this, _Backbuffer_buffers, "f")[1];
    }
    resize(width, height) {
      if (width === __classPrivateFieldGet3(this, _Backbuffer_width, "f") && height === __classPrivateFieldGet3(this, _Backbuffer_height, "f")) {
        return;
      }
      __classPrivateFieldSet3(this, _Backbuffer_width, width, "f");
      __classPrivateFieldSet3(this, _Backbuffer_height, height, "f");
      const pw = width * __classPrivateFieldGet3(this, _Backbuffer_pixelRatio, "f");
      const ph = height * __classPrivateFieldGet3(this, _Backbuffer_pixelRatio, "f");
      __classPrivateFieldGet3(this, _Backbuffer_buffers, "f")[0].setSize(pw, ph);
      __classPrivateFieldGet3(this, _Backbuffer_buffers, "f")[1].setSize(pw, ph);
    }
    /** Rotate the double-buffers. Call after rendering to `target`. */
    swap() {
      __classPrivateFieldSet3(this, _Backbuffer_buffers, [__classPrivateFieldGet3(this, _Backbuffer_buffers, "f")[1], __classPrivateFieldGet3(this, _Backbuffer_buffers, "f")[0]], "f");
    }
    getViewport() {
      return getGLRect(0, 0, __classPrivateFieldGet3(this, _Backbuffer_width, "f"), __classPrivateFieldGet3(this, _Backbuffer_height, "f"));
    }
    dispose() {
      __classPrivateFieldGet3(this, _Backbuffer_buffers, "f")[0].dispose();
      __classPrivateFieldGet3(this, _Backbuffer_buffers, "f")[1].dispose();
    }
  };
  _Backbuffer_width = /* @__PURE__ */ new WeakMap(), _Backbuffer_height = /* @__PURE__ */ new WeakMap(), _Backbuffer_pixelRatio = /* @__PURE__ */ new WeakMap(), _Backbuffer_buffers = /* @__PURE__ */ new WeakMap();

  // node_modules/@vfx-js/core/lib/esm/gl/vec.js
  var Vec2 = class {
    constructor(x = 0, y = 0) {
      this.x = 0;
      this.y = 0;
      this.x = x;
      this.y = y;
    }
    set(x, y) {
      this.x = x;
      this.y = y;
      return this;
    }
  };
  var Vec4 = class {
    constructor(x = 0, y = 0, z = 0, w = 0) {
      this.x = 0;
      this.y = 0;
      this.z = 0;
      this.w = 0;
      this.x = x;
      this.y = y;
      this.z = z;
      this.w = w;
    }
    set(x, y, z, w) {
      this.x = x;
      this.y = y;
      this.z = z;
      this.w = w;
      return this;
    }
  };

  // node_modules/@vfx-js/core/lib/esm/gl/program.js
  var __classPrivateFieldSet4 = function(receiver, state2, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state2.set(receiver, value), value;
  };
  var __classPrivateFieldGet4 = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _Program_instances;
  var _Program_ctx;
  var _Program_vertSrc;
  var _Program_fragSrc;
  var _Program_glslVersion;
  var _Program_uniforms;
  var _Program_compile;
  function detectGlslVersion(src) {
    if (/#version\s+300\s+es\b/.test(src)) {
      return "300 es";
    }
    if (/#version\s+100\b/.test(src)) {
      return "100";
    }
    if (/\bgl_FragColor\b|\btexture2D\b|\bvarying\b|\battribute\b/.test(src)) {
      return "100";
    }
    return "300 es";
  }
  var Program = class {
    constructor(ctx, vertSrc, fragSrc, glslVersion) {
      _Program_instances.add(this);
      _Program_ctx.set(this, void 0);
      _Program_vertSrc.set(this, void 0);
      _Program_fragSrc.set(this, void 0);
      _Program_glslVersion.set(this, void 0);
      _Program_uniforms.set(this, /* @__PURE__ */ new Map());
      __classPrivateFieldSet4(this, _Program_ctx, ctx, "f");
      this.gl = ctx.gl;
      __classPrivateFieldSet4(this, _Program_vertSrc, vertSrc, "f");
      __classPrivateFieldSet4(this, _Program_fragSrc, fragSrc, "f");
      __classPrivateFieldSet4(this, _Program_glslVersion, glslVersion != null ? glslVersion : detectGlslVersion(fragSrc), "f");
      __classPrivateFieldGet4(this, _Program_instances, "m", _Program_compile).call(this);
      ctx.addResource(this);
    }
    restore() {
      __classPrivateFieldGet4(this, _Program_instances, "m", _Program_compile).call(this);
    }
    use() {
      this.gl.useProgram(this.program);
    }
    hasUniform(name) {
      return __classPrivateFieldGet4(this, _Program_uniforms, "f").has(name);
    }
    /** Upload a set of uniforms. Samplers auto-allocate texture units. */
    uploadUniforms(uniforms) {
      const gl = this.gl;
      let textureUnit = 0;
      for (const [name, info] of __classPrivateFieldGet4(this, _Program_uniforms, "f")) {
        const entry = uniforms[name];
        if (!entry) {
          continue;
        }
        const value = entry.value;
        if (value === null || value === void 0) {
          continue;
        }
        if (isSamplerType(info.type)) {
          if (value instanceof Texture) {
            value.bind(textureUnit);
            gl.uniform1i(info.location, textureUnit);
            textureUnit++;
          }
          continue;
        }
        if (value instanceof Texture) {
          continue;
        }
        uploadScalarUniform(gl, info, value);
      }
    }
    dispose() {
      __classPrivateFieldGet4(this, _Program_ctx, "f").removeResource(this);
      this.gl.deleteProgram(this.program);
    }
  };
  _Program_ctx = /* @__PURE__ */ new WeakMap(), _Program_vertSrc = /* @__PURE__ */ new WeakMap(), _Program_fragSrc = /* @__PURE__ */ new WeakMap(), _Program_glslVersion = /* @__PURE__ */ new WeakMap(), _Program_uniforms = /* @__PURE__ */ new WeakMap(), _Program_instances = /* @__PURE__ */ new WeakSet(), _Program_compile = function _Program_compile2() {
    var _a;
    const gl = this.gl;
    const vs = compileShader(gl, gl.VERTEX_SHADER, ensureVersion(__classPrivateFieldGet4(this, _Program_vertSrc, "f"), __classPrivateFieldGet4(this, _Program_glslVersion, "f")));
    const fs = compileShader(gl, gl.FRAGMENT_SHADER, ensureVersion(__classPrivateFieldGet4(this, _Program_fragSrc, "f"), __classPrivateFieldGet4(this, _Program_glslVersion, "f")));
    const program = gl.createProgram();
    if (!program) {
      throw new Error("[VFX-JS] Failed to create program");
    }
    gl.attachShader(program, vs);
    gl.attachShader(program, fs);
    gl.bindAttribLocation(program, 0, "position");
    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      const log = (_a = gl.getProgramInfoLog(program)) != null ? _a : "";
      gl.deleteShader(vs);
      gl.deleteShader(fs);
      gl.deleteProgram(program);
      throw new Error(`[VFX-JS] Program link failed: ${log}`);
    }
    gl.detachShader(program, vs);
    gl.detachShader(program, fs);
    gl.deleteShader(vs);
    gl.deleteShader(fs);
    this.program = program;
    __classPrivateFieldGet4(this, _Program_uniforms, "f").clear();
    const count = gl.getProgramParameter(program, gl.ACTIVE_UNIFORMS);
    for (let i = 0; i < count; i++) {
      const info = gl.getActiveUniform(program, i);
      if (!info) {
        continue;
      }
      const name = info.name.replace(/\[0\]$/, "");
      const location2 = gl.getUniformLocation(program, info.name);
      if (!location2) {
        continue;
      }
      __classPrivateFieldGet4(this, _Program_uniforms, "f").set(name, {
        location: location2,
        type: info.type,
        size: info.size
      });
    }
  };
  function compileShader(gl, type, src) {
    var _a;
    const sh = gl.createShader(type);
    if (!sh) {
      throw new Error("[VFX-JS] Failed to create shader");
    }
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      const log = (_a = gl.getShaderInfoLog(sh)) != null ? _a : "";
      gl.deleteShader(sh);
      throw new Error(`[VFX-JS] Shader compile failed: ${log}

${src}`);
    }
    return sh;
  }
  function ensureVersion(src, version) {
    const trimmed = src.replace(/^\s+/, "");
    if (trimmed.startsWith("#version")) {
      return src;
    }
    if (version === "100") {
      return src;
    }
    return `#version 300 es
${src}`;
  }
  function isSamplerType(type) {
    return type === 35678 || // SAMPLER_2D
    type === 36298 || // INT_SAMPLER_2D
    type === 36306 || // UNSIGNED_INT_SAMPLER_2D
    type === 35682;
  }
  var warnedUnsupportedTypes = /* @__PURE__ */ new Set();
  function uploadScalarUniform(gl, info, value) {
    const loc = info.location;
    const isArray = info.size > 1;
    const fv = value;
    const iv = value;
    const uv = value;
    switch (info.type) {
      case gl.FLOAT:
        if (isArray) {
          gl.uniform1fv(loc, fv);
        } else {
          gl.uniform1f(loc, value);
        }
        return;
      case gl.FLOAT_VEC2:
        if (isArray) {
          gl.uniform2fv(loc, fv);
        } else if (value instanceof Vec2) {
          gl.uniform2f(loc, value.x, value.y);
        } else {
          const v = value;
          gl.uniform2f(loc, v[0], v[1]);
        }
        return;
      case gl.FLOAT_VEC3:
        if (isArray) {
          gl.uniform3fv(loc, fv);
        } else {
          const v = value;
          gl.uniform3f(loc, v[0], v[1], v[2]);
        }
        return;
      case gl.FLOAT_VEC4:
        if (isArray) {
          gl.uniform4fv(loc, fv);
        } else if (value instanceof Vec4) {
          gl.uniform4f(loc, value.x, value.y, value.z, value.w);
        } else {
          const v = value;
          gl.uniform4f(loc, v[0], v[1], v[2], v[3]);
        }
        return;
      case gl.INT:
        if (isArray) {
          gl.uniform1iv(loc, iv);
        } else {
          gl.uniform1i(loc, value);
        }
        return;
      case gl.INT_VEC2:
        if (isArray) {
          gl.uniform2iv(loc, iv);
        } else {
          const v = value;
          gl.uniform2i(loc, v[0], v[1]);
        }
        return;
      case gl.INT_VEC3:
        if (isArray) {
          gl.uniform3iv(loc, iv);
        } else {
          const v = value;
          gl.uniform3i(loc, v[0], v[1], v[2]);
        }
        return;
      case gl.INT_VEC4:
        if (isArray) {
          gl.uniform4iv(loc, iv);
        } else {
          const v = value;
          gl.uniform4i(loc, v[0], v[1], v[2], v[3]);
        }
        return;
      case gl.BOOL:
        if (isArray) {
          gl.uniform1iv(loc, iv);
        } else {
          gl.uniform1i(loc, value ? 1 : 0);
        }
        return;
      case gl.BOOL_VEC2:
        if (isArray) {
          gl.uniform2iv(loc, iv);
        } else {
          const v = value;
          gl.uniform2i(loc, v[0] ? 1 : 0, v[1] ? 1 : 0);
        }
        return;
      case gl.BOOL_VEC3:
        if (isArray) {
          gl.uniform3iv(loc, iv);
        } else {
          const v = value;
          gl.uniform3i(loc, v[0] ? 1 : 0, v[1] ? 1 : 0, v[2] ? 1 : 0);
        }
        return;
      case gl.BOOL_VEC4:
        if (isArray) {
          gl.uniform4iv(loc, iv);
        } else {
          const v = value;
          gl.uniform4i(loc, v[0] ? 1 : 0, v[1] ? 1 : 0, v[2] ? 1 : 0, v[3] ? 1 : 0);
        }
        return;
      case gl.FLOAT_MAT2:
        gl.uniformMatrix2fv(loc, false, fv);
        return;
      case gl.FLOAT_MAT3:
        gl.uniformMatrix3fv(loc, false, fv);
        return;
      case gl.FLOAT_MAT4:
        gl.uniformMatrix4fv(loc, false, fv);
        return;
      case gl.UNSIGNED_INT:
        if (isArray) {
          gl.uniform1uiv(loc, uv);
        } else {
          gl.uniform1ui(loc, value);
        }
        return;
      case gl.UNSIGNED_INT_VEC2:
        if (isArray) {
          gl.uniform2uiv(loc, uv);
        } else {
          const v = value;
          gl.uniform2ui(loc, v[0], v[1]);
        }
        return;
      case gl.UNSIGNED_INT_VEC3:
        if (isArray) {
          gl.uniform3uiv(loc, uv);
        } else {
          const v = value;
          gl.uniform3ui(loc, v[0], v[1], v[2]);
        }
        return;
      case gl.UNSIGNED_INT_VEC4:
        if (isArray) {
          gl.uniform4uiv(loc, uv);
        } else {
          const v = value;
          gl.uniform4ui(loc, v[0], v[1], v[2], v[3]);
        }
        return;
      default:
        if (!warnedUnsupportedTypes.has(info.type)) {
          warnedUnsupportedTypes.add(info.type);
          console.warn(`[VFX-JS] Unsupported uniform type 0x${info.type.toString(16)}; skipping upload.`);
        }
        return;
    }
  }

  // node_modules/@vfx-js/core/lib/esm/gl/pass.js
  var Pass = class {
    constructor(ctx, vertSrc, fragSrc, uniforms, blend, glslVersion) {
      this.gl = ctx.gl;
      this.program = new Program(ctx, vertSrc, fragSrc, glslVersion);
      this.uniforms = uniforms;
      this.blend = blend;
    }
    dispose() {
      this.program.dispose();
    }
  };
  function renderPass(gl, quad, pass, target, viewport, canvasW, canvasH, pixelRatio) {
    const targetCssW = target ? target.width / pixelRatio : canvasW;
    const targetCssH = target ? target.height / pixelRatio : canvasH;
    const cx1 = Math.max(0, viewport.x);
    const cy1 = Math.max(0, viewport.y);
    const cx2 = Math.min(targetCssW, viewport.x + viewport.w);
    const cy2 = Math.min(targetCssH, viewport.y + viewport.h);
    const cw = cx2 - cx1;
    const ch = cy2 - cy1;
    if (cw <= 0 || ch <= 0) {
      return;
    }
    gl.bindFramebuffer(gl.FRAMEBUFFER, target ? target.fbo : null);
    gl.viewport(Math.round(cx1 * pixelRatio), Math.round(cy1 * pixelRatio), Math.round(cw * pixelRatio), Math.round(ch * pixelRatio));
    applyBlend(gl, pass.blend);
    pass.program.use();
    pass.program.uploadUniforms(pass.uniforms);
    quad.draw();
  }
  function applyBlend(gl, mode) {
    if (mode === "none") {
      gl.disable(gl.BLEND);
      return;
    }
    gl.enable(gl.BLEND);
    gl.blendEquation(gl.FUNC_ADD);
    if (mode === "premultiplied") {
      gl.blendFuncSeparate(gl.ONE, gl.ONE_MINUS_SRC_ALPHA, gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    } else if (mode === "additive") {
      gl.blendFuncSeparate(gl.ONE, gl.ONE, gl.ONE, gl.ONE);
    } else {
      gl.blendFuncSeparate(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA, gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    }
  }

  // node_modules/@vfx-js/core/lib/esm/copy-pass.js
  var CopyPass = class {
    constructor(ctx) {
      this.uniforms = {
        src: { value: null },
        offset: { value: new Vec2() },
        resolution: { value: new Vec2() },
        viewport: { value: new Vec4() }
      };
      this.pass = new Pass(ctx, DEFAULT_VERTEX_SHADER, COPY_FRAGMENT_SHADER, this.uniforms, "premultiplied");
    }
    setUniforms(tex, pixelRatio, xywh) {
      this.uniforms.src.value = tex;
      this.uniforms.resolution.value.set(xywh.w * pixelRatio, xywh.h * pixelRatio);
      this.uniforms.offset.value.set(xywh.x * pixelRatio, xywh.y * pixelRatio);
    }
    dispose() {
      this.pass.dispose();
    }
  };

  // node_modules/@vfx-js/core/lib/esm/dom-to-canvas.js
  var convertHtmlToXml = (html) => {
    const doc = document.implementation.createHTMLDocument("test");
    const range = doc.createRange();
    range.selectNodeContents(doc.documentElement);
    range.deleteContents();
    const h = document.createElement("head");
    doc.documentElement.appendChild(h);
    doc.documentElement.appendChild(range.createContextualFragment(html));
    doc.documentElement.setAttribute(
      "xmlns",
      // biome-ignore lint/style/noNonNullAssertion: ok
      doc.documentElement.namespaceURI
    );
    const wfHtml = new XMLSerializer().serializeToString(doc);
    return wfHtml.replace(/<!DOCTYPE html>/, "");
  };
  async function getCanvasFromElement(element, originalOpacity, oldCanvas, maxSize) {
    const rect = element.getBoundingClientRect();
    const ratio = window.devicePixelRatio;
    const ceilW = Math.ceil(rect.width);
    const ceilH = Math.ceil(rect.height);
    const fullW = ceilW * ratio;
    const fullH = ceilH * ratio;
    let clampScale = 1;
    let canvasW = fullW;
    let canvasH = fullH;
    if (maxSize && (canvasW > maxSize || canvasH > maxSize)) {
      clampScale = Math.min(maxSize / canvasW, maxSize / canvasH);
      canvasW = Math.floor(canvasW * clampScale);
      canvasH = Math.floor(canvasH * clampScale);
    }
    const canvas = oldCanvas && oldCanvas.width === canvasW && oldCanvas.height === canvasH ? oldCanvas : new OffscreenCanvas(canvasW, canvasH);
    const newElement = element.cloneNode(true);
    await syncStylesOfTree(element, newElement);
    restoreAutoMargins(element, newElement);
    newElement.style.setProperty("opacity", originalOpacity.toString());
    newElement.style.setProperty("margin", "0px");
    zeroCollapsingMargins(newElement);
    newElement.style.setProperty("box-sizing", "border-box");
    newElement.style.setProperty("width", `${ceilW}px`);
    newElement.style.setProperty("height", `${ceilH}px`);
    const html = newElement.outerHTML;
    const xml = convertHtmlToXml(html);
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${fullW}" height="${fullH}"><foreignObject width="100%" height="100%">${xml}</foreignObject></svg>`;
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => {
        const ctx = canvas.getContext("2d");
        if (ctx === null) {
          return reject();
        }
        ctx.clearRect(0, 0, canvasW, canvasH);
        const drawScale = ratio * clampScale;
        ctx.scale(drawScale, drawScale);
        ctx.drawImage(img, 0, 0, fullW, fullH);
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        resolve(canvas);
      };
      img.src = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
    });
  }
  async function syncStylesOfTree(el1, el2) {
    const styles = window.getComputedStyle(el1);
    for (const key of Array.from(styles)) {
      if (/(-inline-|-block-|^inline-|^block-)/.test(key) || /^-webkit-.*(start|end|before|after|logical)/.test(key)) {
        continue;
      }
      el2.style.setProperty(key, styles.getPropertyValue(key), styles.getPropertyPriority(key));
    }
    if (el2.tagName === "INPUT") {
      el2.setAttribute("value", el2.value);
    } else if (el2.tagName === "TEXTAREA") {
      el2.innerHTML = el2.value;
    } else if (el2.tagName === "IMG") {
      try {
        el2.src = await toObjectUrl(el1.src);
      } catch (e) {
      }
    }
    for (let i = 0; i < el1.children.length; i++) {
      const c1 = el1.children[i];
      const c2 = el2.children[i];
      await syncStylesOfTree(c1, c2);
    }
  }
  function restoreAutoMargins(original, clone) {
    if (typeof original.computedStyleMap === "function") {
      try {
        const map = original.computedStyleMap();
        for (const prop of [
          "margin-top",
          "margin-right",
          "margin-bottom",
          "margin-left"
        ]) {
          const val = map.get(prop);
          if (val instanceof CSSKeywordValue && val.value === "auto") {
            clone.style.setProperty(prop, "auto");
          }
        }
      } catch (e) {
      }
    }
    for (let i = 0; i < original.children.length; i++) {
      const c1 = original.children[i];
      const c2 = clone.children[i];
      if (c1 instanceof HTMLElement && c2 instanceof HTMLElement) {
        restoreAutoMargins(c1, c2);
      }
    }
  }
  function zeroCollapsingMargins(root) {
    let el = root;
    for (; ; ) {
      const s = el.style;
      if (Number.parseFloat(s.paddingTop) > 0 || Number.parseFloat(s.borderTopWidth) > 0 || s.getPropertyValue("overflow-x") && s.getPropertyValue("overflow-x") !== "visible" || s.getPropertyValue("overflow-y") && s.getPropertyValue("overflow-y") !== "visible" || s.display === "flex" || s.display === "grid" || s.display === "flow-root" || s.display === "inline-block") {
        break;
      }
      const child = el.firstElementChild;
      if (!child) {
        break;
      }
      child.style.setProperty("margin-top", "0px");
      el = child;
    }
    el = root;
    for (; ; ) {
      const s = el.style;
      if (Number.parseFloat(s.paddingBottom) > 0 || Number.parseFloat(s.borderBottomWidth) > 0 || s.getPropertyValue("overflow-x") && s.getPropertyValue("overflow-x") !== "visible" || s.getPropertyValue("overflow-y") && s.getPropertyValue("overflow-y") !== "visible" || s.display === "flex" || s.display === "grid" || s.display === "flow-root" || s.display === "inline-block") {
        break;
      }
      const child = el.lastElementChild;
      if (!child) {
        break;
      }
      child.style.setProperty("margin-bottom", "0px");
      el = child;
    }
  }
  async function toObjectUrl(url) {
    const blob = await fetch(url).then((response) => response.blob());
    return new Promise((callback) => {
      const reader = new FileReader();
      reader.onload = function() {
        callback(this.result);
      };
      reader.readAsDataURL(blob);
    });
  }

  // node_modules/@vfx-js/core/lib/esm/effect-geometry.js
  var __classPrivateFieldSet5 = function(receiver, state2, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state2.set(receiver, value), value;
  };
  var __classPrivateFieldGet5 = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _CompiledGeometry_instances;
  var _CompiledGeometry_ctx;
  var _CompiledGeometry_geo;
  var _CompiledGeometry_program;
  var _CompiledGeometry_vbos;
  var _CompiledGeometry_ibo;
  var _CompiledGeometry_registered;
  var _CompiledGeometry_allocate;
  var _EffectGeometryCache_ctx;
  var _EffectGeometryCache_quad;
  var _EffectGeometryCache_map;
  var _EffectGeometryCache_all;
  var EFFECT_QUAD_TOKEN = Object.freeze({
    __brand: "EffectQuad"
  });
  function isEffectQuad(g) {
    return g === EFFECT_QUAD_TOKEN;
  }
  function modeEnum(gl, mode) {
    switch (mode) {
      case "lines":
        return gl.LINES;
      case "lineStrip":
        return gl.LINE_STRIP;
      case "points":
        return gl.POINTS;
      default:
        return gl.TRIANGLES;
    }
  }
  function attribTypeEnum(gl, data) {
    if (data instanceof Float32Array) {
      return gl.FLOAT;
    }
    if (data instanceof Uint8Array) {
      return gl.UNSIGNED_BYTE;
    }
    if (data instanceof Uint16Array) {
      return gl.UNSIGNED_SHORT;
    }
    if (data instanceof Uint32Array) {
      return gl.UNSIGNED_INT;
    }
    if (data instanceof Int8Array) {
      return gl.BYTE;
    }
    if (data instanceof Int16Array) {
      return gl.SHORT;
    }
    if (data instanceof Int32Array) {
      return gl.INT;
    }
    throw new Error("[VFX-JS] Unsupported attribute typed array");
  }
  function normalizeAttribute(name, desc) {
    var _a, _b;
    if (ArrayBuffer.isView(desc) && !(desc instanceof DataView)) {
      return {
        name,
        data: desc,
        itemSize: 2,
        normalized: false,
        perInstance: false
      };
    }
    const d = desc;
    return {
      name,
      data: d.data,
      itemSize: d.itemSize,
      normalized: (_a = d.normalized) != null ? _a : false,
      perInstance: (_b = d.perInstance) != null ? _b : false
    };
  }
  var CompiledGeometry = class {
    constructor(ctx, geo, program) {
      var _a;
      _CompiledGeometry_instances.add(this);
      _CompiledGeometry_ctx.set(this, void 0);
      _CompiledGeometry_geo.set(this, void 0);
      _CompiledGeometry_program.set(this, void 0);
      _CompiledGeometry_vbos.set(this, []);
      _CompiledGeometry_ibo.set(this, null);
      this.indexType = 0;
      this.hasIndices = false;
      this.drawCount = 0;
      this.drawStart = 0;
      _CompiledGeometry_registered.set(this, false);
      __classPrivateFieldSet5(this, _CompiledGeometry_ctx, ctx, "f");
      this.gl = ctx.gl;
      __classPrivateFieldSet5(this, _CompiledGeometry_geo, geo, "f");
      __classPrivateFieldSet5(this, _CompiledGeometry_program, program, "f");
      this.mode = modeEnum(this.gl, geo.mode);
      this.instanceCount = (_a = geo.instanceCount) != null ? _a : 0;
      __classPrivateFieldGet5(this, _CompiledGeometry_instances, "m", _CompiledGeometry_allocate).call(this);
      ctx.addResource(this);
      __classPrivateFieldSet5(this, _CompiledGeometry_registered, true, "f");
    }
    restore() {
      __classPrivateFieldSet5(this, _CompiledGeometry_vbos, [], "f");
      __classPrivateFieldSet5(this, _CompiledGeometry_ibo, null, "f");
      __classPrivateFieldGet5(this, _CompiledGeometry_instances, "m", _CompiledGeometry_allocate).call(this);
    }
    draw() {
      const gl = this.gl;
      gl.bindVertexArray(this.vao);
      if (this.hasIndices) {
        if (this.instanceCount > 0) {
          gl.drawElementsInstanced(this.mode, this.drawCount, this.indexType, this.drawStart * (this.indexType === gl.UNSIGNED_INT ? 4 : 2), this.instanceCount);
        } else {
          gl.drawElements(this.mode, this.drawCount, this.indexType, this.drawStart * (this.indexType === gl.UNSIGNED_INT ? 4 : 2));
        }
      } else if (this.instanceCount > 0) {
        gl.drawArraysInstanced(this.mode, this.drawStart, this.drawCount, this.instanceCount);
      } else {
        gl.drawArrays(this.mode, this.drawStart, this.drawCount);
      }
    }
    dispose() {
      if (__classPrivateFieldGet5(this, _CompiledGeometry_registered, "f")) {
        __classPrivateFieldGet5(this, _CompiledGeometry_ctx, "f").removeResource(this);
        __classPrivateFieldSet5(this, _CompiledGeometry_registered, false, "f");
      }
      const gl = this.gl;
      gl.deleteVertexArray(this.vao);
      for (const b of __classPrivateFieldGet5(this, _CompiledGeometry_vbos, "f")) {
        gl.deleteBuffer(b);
      }
      if (__classPrivateFieldGet5(this, _CompiledGeometry_ibo, "f")) {
        gl.deleteBuffer(__classPrivateFieldGet5(this, _CompiledGeometry_ibo, "f"));
      }
      __classPrivateFieldSet5(this, _CompiledGeometry_vbos, [], "f");
      __classPrivateFieldSet5(this, _CompiledGeometry_ibo, null, "f");
    }
  };
  _CompiledGeometry_ctx = /* @__PURE__ */ new WeakMap(), _CompiledGeometry_geo = /* @__PURE__ */ new WeakMap(), _CompiledGeometry_program = /* @__PURE__ */ new WeakMap(), _CompiledGeometry_vbos = /* @__PURE__ */ new WeakMap(), _CompiledGeometry_ibo = /* @__PURE__ */ new WeakMap(), _CompiledGeometry_registered = /* @__PURE__ */ new WeakMap(), _CompiledGeometry_instances = /* @__PURE__ */ new WeakSet(), _CompiledGeometry_allocate = function _CompiledGeometry_allocate2() {
    var _a;
    const gl = this.gl;
    const vao = gl.createVertexArray();
    if (!vao) {
      throw new Error("[VFX-JS] Failed to create VAO");
    }
    this.vao = vao;
    gl.bindVertexArray(vao);
    const programHandle = __classPrivateFieldGet5(this, _CompiledGeometry_program, "f").program;
    let vertexCountFromPosition = null;
    for (const [name, descriptor] of Object.entries(__classPrivateFieldGet5(this, _CompiledGeometry_geo, "f").attributes)) {
      const attr = normalizeAttribute(name, descriptor);
      const loc = gl.getAttribLocation(programHandle, attr.name);
      if (loc < 0) {
        continue;
      }
      const buffer = gl.createBuffer();
      if (!buffer) {
        throw new Error(`[VFX-JS] Failed to create VBO for "${attr.name}"`);
      }
      __classPrivateFieldGet5(this, _CompiledGeometry_vbos, "f").push(buffer);
      gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
      gl.bufferData(gl.ARRAY_BUFFER, attr.data, gl.STATIC_DRAW);
      const type = attribTypeEnum(gl, attr.data);
      gl.enableVertexAttribArray(loc);
      if (type === gl.FLOAT || type === gl.HALF_FLOAT || attr.normalized) {
        gl.vertexAttribPointer(loc, attr.itemSize, type, attr.normalized, 0, 0);
      } else {
        gl.vertexAttribIPointer(loc, attr.itemSize, type, 0, 0);
      }
      if (attr.perInstance) {
        gl.vertexAttribDivisor(loc, 1);
      }
      if (name === "position" && vertexCountFromPosition === null) {
        vertexCountFromPosition = attr.data.length / attr.itemSize;
      }
    }
    let indexCount = 0;
    const indices = __classPrivateFieldGet5(this, _CompiledGeometry_geo, "f").indices;
    if (indices) {
      const ibo = gl.createBuffer();
      if (!ibo) {
        throw new Error("[VFX-JS] Failed to create IBO");
      }
      __classPrivateFieldSet5(this, _CompiledGeometry_ibo, ibo, "f");
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo);
      gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW);
      this.hasIndices = true;
      this.indexType = indices instanceof Uint32Array ? gl.UNSIGNED_INT : gl.UNSIGNED_SHORT;
      indexCount = indices.length;
    } else {
      this.hasIndices = false;
    }
    gl.bindVertexArray(null);
    gl.bindBuffer(gl.ARRAY_BUFFER, null);
    if (__classPrivateFieldGet5(this, _CompiledGeometry_ibo, "f")) {
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, null);
    }
    const totalCount = this.hasIndices ? indexCount : vertexCountFromPosition != null ? vertexCountFromPosition : 0;
    const range = __classPrivateFieldGet5(this, _CompiledGeometry_geo, "f").drawRange;
    this.drawStart = (_a = range == null ? void 0 : range.start) != null ? _a : 0;
    this.drawCount = (range == null ? void 0 : range.count) !== void 0 ? range.count : Math.max(0, totalCount - this.drawStart);
  };
  var EffectGeometryCache = class {
    constructor(ctx, quad) {
      _EffectGeometryCache_ctx.set(this, void 0);
      _EffectGeometryCache_quad.set(this, void 0);
      _EffectGeometryCache_map.set(this, /* @__PURE__ */ new WeakMap());
      _EffectGeometryCache_all.set(this, /* @__PURE__ */ new Set());
      __classPrivateFieldSet5(this, _EffectGeometryCache_ctx, ctx, "f");
      __classPrivateFieldSet5(this, _EffectGeometryCache_quad, quad, "f");
    }
    /** The shared fullscreen {@link Quad} (resolves {@link EFFECT_QUAD_TOKEN}). */
    get quad() {
      return __classPrivateFieldGet5(this, _EffectGeometryCache_quad, "f");
    }
    resolve(geo, program) {
      let byProgram = __classPrivateFieldGet5(this, _EffectGeometryCache_map, "f").get(geo);
      if (!byProgram) {
        byProgram = /* @__PURE__ */ new Map();
        __classPrivateFieldGet5(this, _EffectGeometryCache_map, "f").set(geo, byProgram);
      }
      let compiled = byProgram.get(program);
      if (!compiled) {
        compiled = new CompiledGeometry(__classPrivateFieldGet5(this, _EffectGeometryCache_ctx, "f"), geo, program);
        byProgram.set(program, compiled);
        __classPrivateFieldGet5(this, _EffectGeometryCache_all, "f").add(compiled);
      }
      return compiled;
    }
    dispose() {
      for (const c of __classPrivateFieldGet5(this, _EffectGeometryCache_all, "f")) {
        c.dispose();
      }
      __classPrivateFieldGet5(this, _EffectGeometryCache_all, "f").clear();
    }
  };
  _EffectGeometryCache_ctx = /* @__PURE__ */ new WeakMap(), _EffectGeometryCache_quad = /* @__PURE__ */ new WeakMap(), _EffectGeometryCache_map = /* @__PURE__ */ new WeakMap(), _EffectGeometryCache_all = /* @__PURE__ */ new WeakMap();

  // node_modules/@vfx-js/core/lib/esm/effect-host.js
  var __classPrivateFieldSet6 = function(receiver, state2, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state2.set(receiver, value), value;
  };
  var __classPrivateFieldGet6 = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _EffectHost_instances;
  var _EffectHost_glCtx;
  var _EffectHost_gl;
  var _EffectHost_pixelRatio;
  var _EffectHost_programCache;
  var _EffectHost_geometries;
  var _EffectHost_ownedTextures;
  var _EffectHost_ownedRTs;
  var _EffectHost_autoResizeRTs;
  var _EffectHost_restoredUnsubs;
  var _EffectHost_phase;
  var _EffectHost_warnedDrawInUpdate;
  var _EffectHost_dims;
  var _EffectHost_mutCtx;
  var _EffectHost_createRenderTarget;
  var _EffectHost_disposeOwnedRT;
  var _EffectHost_wrapTexture;
  var _EffectHost_perFrameAutoUpdate;
  var _EffectHost_draw;
  var _EffectHost_blit;
  var _EffectHost_doDraw;
  var _EffectHost_buildUniforms;
  var RESOLVE_TEXTURE = Symbol.for("@vfx-js/effect.resolve-texture");
  var RESOLVE_RT = Symbol.for("@vfx-js/effect.resolve-rt");
  function resolveTexture(h) {
    return h[RESOLVE_TEXTURE]();
  }
  function resolveRt(h) {
    return h[RESOLVE_RT];
  }
  var DEFAULT_VERT_300 = `#version 300 es
precision highp float;
in vec3 position;
out vec2 uv;
out vec2 uvContent;
out vec2 uvSrc;
uniform vec4 contentRectUv;
uniform vec4 srcRectUv;
void main() {
    vec2 bufferUV = position.xy * 0.5 + 0.5;
    uv = bufferUV;
    uvContent = (bufferUV - contentRectUv.xy) / contentRectUv.zw;
    uvSrc = srcRectUv.xy + uvContent * srcRectUv.zw;
    gl_Position = vec4(position, 1.0);
}
`;
  var DEFAULT_VERT_100 = `
precision highp float;
attribute vec3 position;
varying vec2 uv;
varying vec2 uvContent;
varying vec2 uvSrc;
uniform vec4 contentRectUv;
uniform vec4 srcRectUv;
void main() {
    vec2 bufferUV = position.xy * 0.5 + 0.5;
    uv = bufferUV;
    uvContent = (bufferUV - contentRectUv.xy) / contentRectUv.zw;
    uvSrc = srcRectUv.xy + uvContent * srcRectUv.zw;
    gl_Position = vec4(position, 1.0);
}
`;
  var PASSTHROUGH_FRAG_300 = `#version 300 es
precision highp float;
in vec2 uv;
out vec4 outColor;
uniform sampler2D src;
void main() {
    outColor = texture(src, uv);
}
`;
  var PASSTHROUGH_FRAG_100 = `
precision highp float;
varying vec2 uv;
uniform sampler2D src;
void main() {
    gl_FragColor = texture2D(src, uv);
}
`;
  var BLIT_FRAG_300 = `#version 300 es
precision highp float;
in vec2 uvSrc;
out vec4 outColor;
uniform sampler2D src;
void main() {
    outColor = texture(src, uvSrc);
}
`;
  var BLIT_FRAG_100 = `
precision highp float;
varying vec2 uvSrc;
uniform sampler2D src;
void main() {
    gl_FragColor = texture2D(src, uvSrc);
}
`;
  var EffectHost = class {
    constructor(glCtx, quad, pixelRatio, initialSrc, initialVfxProps, programCache) {
      _EffectHost_instances.add(this);
      _EffectHost_glCtx.set(this, void 0);
      _EffectHost_gl.set(this, void 0);
      _EffectHost_pixelRatio.set(this, void 0);
      _EffectHost_programCache.set(this, void 0);
      _EffectHost_geometries.set(this, void 0);
      _EffectHost_ownedTextures.set(this, []);
      _EffectHost_ownedRTs.set(this, []);
      _EffectHost_autoResizeRTs.set(this, []);
      _EffectHost_restoredUnsubs.set(this, []);
      _EffectHost_phase.set(this, "init");
      _EffectHost_warnedDrawInUpdate.set(this, false);
      _EffectHost_dims.set(this, void 0);
      _EffectHost_mutCtx.set(this, void 0);
      _EffectHost_perFrameAutoUpdate.set(this, []);
      __classPrivateFieldSet6(this, _EffectHost_glCtx, glCtx, "f");
      __classPrivateFieldSet6(this, _EffectHost_gl, glCtx.gl, "f");
      __classPrivateFieldSet6(this, _EffectHost_pixelRatio, pixelRatio, "f");
      __classPrivateFieldSet6(this, _EffectHost_programCache, programCache, "f");
      __classPrivateFieldSet6(this, _EffectHost_geometries, new EffectGeometryCache(glCtx, quad), "f");
      __classPrivateFieldSet6(this, _EffectHost_dims, {
        outputBufferW: 1,
        outputBufferH: 1,
        canvasBufferSize: [1, 1],
        outputViewport: { x: 0, y: 0, w: 1, h: 1 },
        elementBufferW: 1,
        elementBufferH: 1,
        contentRectUv: [0, 0, 1, 1],
        srcRectUv: [0, 0, 1, 1]
      }, "f");
      const initialDims = {
        element: [1, 1],
        elementPixel: [1, 1],
        canvas: [1, 1],
        canvasPixel: [1, 1],
        pixelRatio,
        contentRect: [0, 0, 1, 1],
        srcRect: [0, 0, 1, 1],
        canvasRect: [0, 0, 1, 1]
      };
      const ctx = {
        time: 0,
        deltaTime: 0,
        pixelRatio,
        resolution: [1, 1],
        mouse: [0, 0],
        mouseViewport: [0, 0],
        intersection: 0,
        enterTime: 0,
        leaveTime: 0,
        src: initialSrc,
        target: null,
        uniforms: {},
        vfxProps: initialVfxProps,
        dims: initialDims,
        quad: EFFECT_QUAD_TOKEN,
        gl: __classPrivateFieldGet6(this, _EffectHost_gl, "f"),
        createRenderTarget: (opts) => __classPrivateFieldGet6(this, _EffectHost_instances, "m", _EffectHost_createRenderTarget).call(this, opts),
        wrapTexture: (source, opts) => __classPrivateFieldGet6(this, _EffectHost_instances, "m", _EffectHost_wrapTexture).call(this, source, opts),
        draw: (opts) => __classPrivateFieldGet6(this, _EffectHost_instances, "m", _EffectHost_draw).call(this, opts),
        blit: (source, target, opts) => __classPrivateFieldGet6(this, _EffectHost_instances, "m", _EffectHost_blit).call(this, source, target, opts),
        onContextRestored: (cb) => {
          const unsub = __classPrivateFieldGet6(this, _EffectHost_glCtx, "f").onContextRestored(cb);
          __classPrivateFieldGet6(this, _EffectHost_restoredUnsubs, "f").push(unsub);
          return unsub;
        }
      };
      __classPrivateFieldSet6(this, _EffectHost_mutCtx, ctx, "f");
    }
    get ctx() {
      return __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f");
    }
    // -- orchestrator-facing API --------------------------------------------
    setPhase(p) {
      __classPrivateFieldSet6(this, _EffectHost_phase, p, "f");
    }
    setFrameDims(dims) {
      var _a, _b;
      __classPrivateFieldSet6(this, _EffectHost_dims, dims, "f");
      __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f").resolution = [
        dims.canvasBufferSize[0],
        dims.canvasBufferSize[1]
      ];
      for (const rt of __classPrivateFieldGet6(this, _EffectHost_autoResizeRTs, "f")) {
        (_b = (_a = rt.resolver).resize) == null ? void 0 : _b.call(_a, dims.outputBufferW, dims.outputBufferH);
      }
    }
    setEffectDims(dims) {
      __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f").dims = dims;
    }
    setFrameState(state2) {
      const c = __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f");
      c.time = state2.time;
      c.deltaTime = state2.deltaTime;
      c.mouse = state2.mouse;
      c.mouseViewport = state2.mouseViewport;
      c.intersection = state2.intersection;
      c.enterTime = state2.enterTime;
      c.leaveTime = state2.leaveTime;
      c.uniforms = state2.uniforms;
    }
    setSrc(src) {
      __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f").src = src;
    }
    setOutput(output) {
      __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f").target = output;
    }
    // -- internal passthrough pass (used by chain for stageCount=0 / fallback)
    /**
     * Draws a passthrough copy of `src` into `target` using the host's
     * own program cache. The viewport passed in is device-px.
     */
    passthroughCopy(src, target, viewport) {
      const prevPhase = __classPrivateFieldGet6(this, _EffectHost_phase, "f");
      __classPrivateFieldSet6(this, _EffectHost_phase, "render", "f");
      const prevOutput = __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f").target;
      __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f").target = target;
      try {
        const prevVp = __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputViewport;
        __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputViewport = __spreadValues({}, viewport);
        const glslVersion = __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f").vfxProps.glslVersion;
        const frag = glslVersion === "100" ? PASSTHROUGH_FRAG_100 : PASSTHROUGH_FRAG_300;
        __classPrivateFieldGet6(this, _EffectHost_instances, "m", _EffectHost_doDraw).call(this, {
          frag,
          uniforms: { src },
          target
        });
        __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputViewport = prevVp;
      } finally {
        __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f").target = prevOutput;
        __classPrivateFieldSet6(this, _EffectHost_phase, prevPhase, "f");
      }
    }
    /** Clears the given RT with `(0, 0, 0, 0)`. Device-px target. */
    clearRt(rt) {
      const gl = __classPrivateFieldGet6(this, _EffectHost_gl, "f");
      const resolver = resolveRt(rt);
      gl.bindFramebuffer(gl.FRAMEBUFFER, resolver.getWriteFbo().fbo);
      gl.viewport(0, 0, rt.width, rt.height);
      gl.clearColor(0, 0, 0, 0);
      gl.disable(gl.SCISSOR_TEST);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    }
    /** Called by the chain at the start of the render phase. */
    tickAutoUpdates() {
      for (const fn of __classPrivateFieldGet6(this, _EffectHost_perFrameAutoUpdate, "f")) {
        fn();
      }
    }
    // -- dispose ------------------------------------------------------------
    dispose() {
      var _a, _b;
      __classPrivateFieldSet6(this, _EffectHost_phase, "disposed", "f");
      for (const unsub of __classPrivateFieldGet6(this, _EffectHost_restoredUnsubs, "f")) {
        unsub();
      }
      __classPrivateFieldSet6(this, _EffectHost_restoredUnsubs, [], "f");
      for (const rt of __classPrivateFieldGet6(this, _EffectHost_ownedRTs, "f")) {
        (_b = (_a = rt.resolver).dispose) == null ? void 0 : _b.call(_a);
      }
      __classPrivateFieldSet6(this, _EffectHost_ownedRTs, [], "f");
      __classPrivateFieldSet6(this, _EffectHost_autoResizeRTs, [], "f");
      for (const t of __classPrivateFieldGet6(this, _EffectHost_ownedTextures, "f")) {
        t.dispose();
      }
      __classPrivateFieldSet6(this, _EffectHost_ownedTextures, [], "f");
      __classPrivateFieldGet6(this, _EffectHost_geometries, "f").dispose();
      __classPrivateFieldSet6(this, _EffectHost_perFrameAutoUpdate, [], "f");
    }
  };
  _EffectHost_glCtx = /* @__PURE__ */ new WeakMap(), _EffectHost_gl = /* @__PURE__ */ new WeakMap(), _EffectHost_pixelRatio = /* @__PURE__ */ new WeakMap(), _EffectHost_programCache = /* @__PURE__ */ new WeakMap(), _EffectHost_geometries = /* @__PURE__ */ new WeakMap(), _EffectHost_ownedTextures = /* @__PURE__ */ new WeakMap(), _EffectHost_ownedRTs = /* @__PURE__ */ new WeakMap(), _EffectHost_autoResizeRTs = /* @__PURE__ */ new WeakMap(), _EffectHost_restoredUnsubs = /* @__PURE__ */ new WeakMap(), _EffectHost_phase = /* @__PURE__ */ new WeakMap(), _EffectHost_warnedDrawInUpdate = /* @__PURE__ */ new WeakMap(), _EffectHost_dims = /* @__PURE__ */ new WeakMap(), _EffectHost_mutCtx = /* @__PURE__ */ new WeakMap(), _EffectHost_perFrameAutoUpdate = /* @__PURE__ */ new WeakMap(), _EffectHost_instances = /* @__PURE__ */ new WeakSet(), _EffectHost_createRenderTarget = function _EffectHost_createRenderTarget2(opts) {
    var _a, _b, _c;
    const persistent = (_a = opts == null ? void 0 : opts.persistent) != null ? _a : false;
    const float = (_b = opts == null ? void 0 : opts.float) != null ? _b : false;
    const wrap = normalizeWrap(opts == null ? void 0 : opts.wrap);
    const filter = opts == null ? void 0 : opts.filter;
    const mipmapOpt = (_c = opts == null ? void 0 : opts.mipmap) != null ? _c : false;
    const mipmap = mipmapOpt !== false;
    const mipmapAutoRegen = mipmapOpt === true;
    const explicitSize = opts == null ? void 0 : opts.size;
    const sizeW = explicitSize ? explicitSize[0] : __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputBufferW;
    const sizeH = explicitSize ? explicitSize[1] : __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputBufferH;
    let resolver;
    let getW;
    let getH;
    if (persistent) {
      const pr = explicitSize ? 1 : __classPrivateFieldGet6(this, _EffectHost_pixelRatio, "f");
      const cssW = explicitSize ? sizeW : sizeW / pr;
      const cssH = explicitSize ? sizeH : sizeH / pr;
      const bb = new Backbuffer(__classPrivateFieldGet6(this, _EffectHost_glCtx, "f"), cssW, cssH, pr, float, {
        wrap,
        filter,
        mipmap
      });
      resolver = {
        getReadTexture: () => bb.texture,
        getWriteFbo: () => bb.target,
        swap: () => bb.swap(),
        resize: explicitSize ? void 0 : (bufferW, bufferH) => {
          bb.resize(bufferW / __classPrivateFieldGet6(this, _EffectHost_pixelRatio, "f"), bufferH / __classPrivateFieldGet6(this, _EffectHost_pixelRatio, "f"));
        },
        dispose: () => bb.dispose()
      };
      if (mipmap) {
        resolver.regenerateMipmaps = () => bb.target.generateMipmaps();
        resolver.mipmapAutoRegen = mipmapAutoRegen;
      }
      getW = () => bb.target.width;
      getH = () => bb.target.height;
    } else {
      const fb = new Framebuffer(__classPrivateFieldGet6(this, _EffectHost_glCtx, "f"), sizeW, sizeH, {
        float,
        wrap,
        filter,
        mipmap
      });
      resolver = {
        getReadTexture: () => fb.texture,
        getWriteFbo: () => fb,
        resize: explicitSize ? void 0 : (bufferW, bufferH) => fb.setSize(bufferW, bufferH),
        dispose: () => fb.dispose()
      };
      if (mipmap) {
        resolver.regenerateMipmaps = () => fb.generateMipmaps();
        resolver.mipmapAutoRegen = mipmapAutoRegen;
      }
      getW = () => fb.width;
      getH = () => fb.height;
    }
    let owned;
    const dispose = () => __classPrivateFieldGet6(this, _EffectHost_instances, "m", _EffectHost_disposeOwnedRT).call(this, owned);
    const handle = makeEffectRenderTarget(resolver, getW, getH, dispose);
    owned = { handle, resolver };
    __classPrivateFieldGet6(this, _EffectHost_ownedRTs, "f").push(owned);
    if (!explicitSize) {
      __classPrivateFieldGet6(this, _EffectHost_autoResizeRTs, "f").push(owned);
    }
    return handle;
  }, _EffectHost_disposeOwnedRT = function _EffectHost_disposeOwnedRT2(owned) {
    var _a, _b;
    const idx = __classPrivateFieldGet6(this, _EffectHost_ownedRTs, "f").indexOf(owned);
    if (idx < 0) {
      return;
    }
    __classPrivateFieldGet6(this, _EffectHost_ownedRTs, "f").splice(idx, 1);
    const aIdx = __classPrivateFieldGet6(this, _EffectHost_autoResizeRTs, "f").indexOf(owned);
    if (aIdx >= 0) {
      __classPrivateFieldGet6(this, _EffectHost_autoResizeRTs, "f").splice(aIdx, 1);
    }
    (_b = (_a = owned.resolver).dispose) == null ? void 0 : _b.call(_a);
  }, _EffectHost_wrapTexture = function _EffectHost_wrapTexture2(source, opts) {
    var _a;
    const wrap = normalizeWrap(opts == null ? void 0 : opts.wrap);
    const filter = opts == null ? void 0 : opts.filter;
    let texture;
    let getW;
    let getH;
    let autoUpdateFn = null;
    const isRawHandle = isWebGLTextureHandle(source);
    if (isRawHandle) {
      if (!(opts == null ? void 0 : opts.size)) {
        throw new Error("[VFX-JS] wrapTexture(WebGLTexture) requires opts.size");
      }
      const [sw, sh] = opts.size;
      texture = new Texture(__classPrivateFieldGet6(this, _EffectHost_glCtx, "f"), void 0, {
        autoRegister: false,
        externalHandle: source
      });
      getW = () => sw;
      getH = () => sh;
    } else {
      const domSource = source;
      texture = new Texture(__classPrivateFieldGet6(this, _EffectHost_glCtx, "f"), domSource);
      const explicitSize = opts == null ? void 0 : opts.size;
      const readDim = (axis) => {
        if (explicitSize) {
          return axis === "w" ? explicitSize[0] : explicitSize[1];
        }
        if (typeof HTMLImageElement !== "undefined" && domSource instanceof HTMLImageElement) {
          return axis === "w" ? domSource.naturalWidth : domSource.naturalHeight;
        }
        if (typeof HTMLVideoElement !== "undefined" && domSource instanceof HTMLVideoElement) {
          return axis === "w" ? domSource.videoWidth : domSource.videoHeight;
        }
        const wc = domSource;
        return axis === "w" ? wc.width : wc.height;
      };
      getW = () => readDim("w");
      getH = () => readDim("h");
      const videoLike = typeof HTMLVideoElement !== "undefined" && domSource instanceof HTMLVideoElement || typeof HTMLCanvasElement !== "undefined" && domSource instanceof HTMLCanvasElement || typeof OffscreenCanvas !== "undefined" && domSource instanceof OffscreenCanvas;
      const autoUpdate = (_a = opts == null ? void 0 : opts.autoUpdate) != null ? _a : videoLike;
      if (autoUpdate) {
        autoUpdateFn = () => {
          texture.needsUpdate = true;
        };
      }
    }
    texture.wrapS = wrap[0];
    texture.wrapT = wrap[1];
    if (filter !== void 0) {
      texture.minFilter = filter;
      texture.magFilter = filter;
    }
    __classPrivateFieldGet6(this, _EffectHost_ownedTextures, "f").push(texture);
    if (autoUpdateFn) {
      __classPrivateFieldGet6(this, _EffectHost_perFrameAutoUpdate, "f").push(autoUpdateFn);
    }
    return makeEffectTexture(() => texture, getW, getH);
  }, _EffectHost_draw = function _EffectHost_draw2(opts) {
    if (__classPrivateFieldGet6(this, _EffectHost_phase, "f") !== "render") {
      if (__classPrivateFieldGet6(this, _EffectHost_phase, "f") === "update" && !__classPrivateFieldGet6(this, _EffectHost_warnedDrawInUpdate, "f")) {
        __classPrivateFieldSet6(this, _EffectHost_warnedDrawInUpdate, true, "f");
        console.warn("[VFX-JS] ctx.draw() called in update(); ignored. Move draws to render().");
      }
      return;
    }
    __classPrivateFieldGet6(this, _EffectHost_instances, "m", _EffectHost_doDraw).call(this, opts);
  }, _EffectHost_blit = function _EffectHost_blit2(source, target, opts) {
    if (__classPrivateFieldGet6(this, _EffectHost_phase, "f") !== "render") {
      if (__classPrivateFieldGet6(this, _EffectHost_phase, "f") === "update" && !__classPrivateFieldGet6(this, _EffectHost_warnedDrawInUpdate, "f")) {
        __classPrivateFieldSet6(this, _EffectHost_warnedDrawInUpdate, true, "f");
        console.warn("[VFX-JS] ctx.blit() called in update(); ignored. Move draws to render().");
      }
      return;
    }
    const frag = __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f").vfxProps.glslVersion === "100" ? BLIT_FRAG_100 : BLIT_FRAG_300;
    __classPrivateFieldGet6(this, _EffectHost_instances, "m", _EffectHost_doDraw).call(this, {
      frag,
      uniforms: { src: source },
      target,
      blend: opts == null ? void 0 : opts.blend,
      swap: opts == null ? void 0 : opts.swap
    });
  }, _EffectHost_doDraw = function _EffectHost_doDraw2(opts) {
    var _a, _b, _c;
    const gl = __classPrivateFieldGet6(this, _EffectHost_gl, "f");
    const vert = (_a = opts.vert) != null ? _a : __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f").vfxProps.glslVersion === "100" ? DEFAULT_VERT_100 : DEFAULT_VERT_300;
    const program = __classPrivateFieldGet6(this, _EffectHost_programCache, "f").get(vert, opts.frag, __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f").vfxProps.glslVersion);
    const ctxOutput = __classPrivateFieldGet6(this, _EffectHost_mutCtx, "f").target;
    const rawTarget = opts.target === void 0 || opts.target === null ? ctxOutput : opts.target;
    const isStageOutput = rawTarget === null || rawTarget === ctxOutput;
    let fbo;
    let vpX;
    let vpY;
    let vpW;
    let vpH;
    let swap;
    let regenerateMipmaps;
    if (rawTarget === null) {
      fbo = null;
      vpX = __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputViewport.x;
      vpY = __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputViewport.y;
      vpW = __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputViewport.w;
      vpH = __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputViewport.h;
    } else {
      const resolver = resolveRt(rawTarget);
      fbo = resolver.getWriteFbo().fbo;
      if (isStageOutput) {
        vpX = __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputViewport.x;
        vpY = __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputViewport.y;
        vpW = __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputViewport.w;
        vpH = __classPrivateFieldGet6(this, _EffectHost_dims, "f").outputViewport.h;
      } else {
        vpX = 0;
        vpY = 0;
        vpW = rawTarget.width;
        vpH = rawTarget.height;
      }
      swap = resolver.swap;
      if (resolver.mipmapAutoRegen) {
        regenerateMipmaps = resolver.regenerateMipmaps;
      }
    }
    gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
    gl.viewport(vpX, vpY, vpW, vpH);
    gl.disable(gl.SCISSOR_TEST);
    const blend = (_b = opts.blend) != null ? _b : rawTarget === null ? "premultiplied" : "none";
    applyBlend(gl, blend);
    program.use();
    const uniforms = __classPrivateFieldGet6(this, _EffectHost_instances, "m", _EffectHost_buildUniforms).call(this, opts.uniforms);
    program.uploadUniforms(uniforms);
    const geometry = (_c = opts.geometry) != null ? _c : EFFECT_QUAD_TOKEN;
    if (isEffectQuad(geometry)) {
      __classPrivateFieldGet6(this, _EffectHost_geometries, "f").quad.draw();
    } else {
      const compiled = __classPrivateFieldGet6(this, _EffectHost_geometries, "f").resolve(geometry, program);
      compiled.draw();
    }
    regenerateMipmaps == null ? void 0 : regenerateMipmaps();
    if (swap && opts.swap !== false) {
      swap();
    }
  }, _EffectHost_buildUniforms = function _EffectHost_buildUniforms2(userUniforms) {
    const out = {};
    out["contentRectUv"] = { value: __classPrivateFieldGet6(this, _EffectHost_dims, "f").contentRectUv };
    out["srcRectUv"] = { value: __classPrivateFieldGet6(this, _EffectHost_dims, "f").srcRectUv };
    if (!userUniforms) {
      return out;
    }
    for (const [name, value] of Object.entries(userUniforms)) {
      out[name] = toInternalUniform(value);
    }
    return out;
  };
  function isWebGLTextureHandle(source) {
    const globalWebGLTexture = globalThis.WebGLTexture;
    if (globalWebGLTexture && typeof globalWebGLTexture === "function" && source instanceof globalWebGLTexture) {
      return true;
    }
    const s = source;
    return s.width === void 0 && s.naturalWidth === void 0 && s.videoWidth === void 0;
  }
  function normalizeWrap(w) {
    if (w === void 0) {
      return ["clamp", "clamp"];
    }
    if (typeof w === "string") {
      return [w, w];
    }
    return [w[0], w[1]];
  }
  function toInternalUniform(value) {
    if (typeof value === "object" && value !== null && "__brand" in value) {
      if (value.__brand === "EffectRenderTarget") {
        return { value: resolveRt(value).getReadTexture() };
      }
      return { value: resolveTexture(value) };
    }
    return { value };
  }
  function makeEffectTexture(resolve, width, height) {
    const handle = {
      __brand: "EffectTexture",
      get width() {
        return width();
      },
      get height() {
        return height();
      }
    };
    Object.defineProperty(handle, RESOLVE_TEXTURE, { value: resolve });
    return handle;
  }
  function makeEffectRenderTarget(resolver, width, height, dispose) {
    const handle = {
      __brand: "EffectRenderTarget",
      get width() {
        return width();
      },
      get height() {
        return height();
      },
      // Framework-owned RTs pass no dispose; the no-op makes
      // `rt.dispose()` always safe to call.
      dispose: dispose != null ? dispose : () => {
      },
      // No-op when the underlying RT has no mip storage.
      generateMipmaps: () => {
        var _a;
        return (_a = resolver.regenerateMipmaps) == null ? void 0 : _a.call(resolver);
      }
    };
    Object.defineProperty(handle, RESOLVE_RT, { value: resolver });
    return handle;
  }
  function makeEffectRenderTargetFromFb(fb) {
    const resolver = {
      getReadTexture: () => fb.texture,
      getWriteFbo: () => fb
    };
    return makeEffectRenderTarget(resolver, () => fb.width, () => fb.height);
  }

  // node_modules/@vfx-js/core/lib/esm/rect.js
  function createTetra(r) {
    var _a, _b, _c, _d;
    if (typeof r === "number") {
      return {
        top: r,
        right: r,
        bottom: r,
        left: r
      };
    }
    if (Array.isArray(r)) {
      return {
        top: r[0],
        right: r[1],
        bottom: r[2],
        left: r[3]
      };
    }
    return {
      top: (_a = r.top) != null ? _a : 0,
      right: (_b = r.right) != null ? _b : 0,
      bottom: (_c = r.bottom) != null ? _c : 0,
      left: (_d = r.left) != null ? _d : 0
    };
  }
  function createMargin(r) {
    return createTetra(r);
  }
  var MARGIN_ZERO = {
    top: 0,
    right: 0,
    bottom: 0,
    left: 0
  };
  function createRect(r) {
    return createTetra(r);
  }
  function toRect(r) {
    return {
      top: r.top,
      right: r.right,
      bottom: r.bottom,
      left: r.left
    };
  }
  function toCeiledRect(r) {
    return {
      top: r.top,
      left: r.left,
      right: r.left + Math.ceil(r.right - r.left),
      bottom: r.top + Math.ceil(r.bottom - r.top)
    };
  }
  function growRect(a, b) {
    return {
      top: a.top - b.top,
      right: a.right + b.right,
      bottom: a.bottom + b.bottom,
      left: a.left - b.left
    };
  }
  function clamp(x, xmin, xmax) {
    return Math.min(Math.max(x, xmin), xmax);
  }
  function rectInRect(inner, outer) {
    const [ix, iy, iw, ih] = inner;
    const [ox, oy, ow, oh] = outer;
    if (ow <= 0 || oh <= 0) {
      return [0, 0, 1, 1];
    }
    return [(ix - ox) / ow, (iy - oy) / oh, iw / ow, ih / oh];
  }
  function getIntersection(container, target) {
    const targetL = clamp(target.left, container.left, container.right);
    const targetR = clamp(target.right, container.left, container.right);
    const w = (targetR - targetL) / (target.right - target.left);
    const targetT = clamp(target.top, container.top, container.bottom);
    const targetB = clamp(target.bottom, container.top, container.bottom);
    const h = (targetB - targetT) / (target.bottom - target.top);
    return w * h;
  }

  // node_modules/@vfx-js/core/lib/esm/effect-chain.js
  var __classPrivateFieldSet7 = function(receiver, state2, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state2.set(receiver, value), value;
  };
  var __classPrivateFieldGet7 = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _EffectChain_instances;
  var _EffectChain_glCtx;
  var _EffectChain_quad;
  var _EffectChain_pixelRatio;
  var _EffectChain_vfxProps;
  var _EffectChain_programCache;
  var _EffectChain_effects;
  var _EffectChain_hosts;
  var _EffectChain_renderingIndices;
  var _EffectChain_intermediates;
  var _EffectChain_stages;
  var _EffectChain_capture;
  var _EffectChain_warnedEffects;
  var _EffectChain_disposed;
  var _EffectChain_isPostEffect;
  var _EffectChain_lastHitTestPad;
  var _EffectChain_ownedPassthroughHost;
  var _EffectChain_computeRenderingIndices;
  var _EffectChain_newHost;
  var _EffectChain_safeDispose;
  var _EffectChain_resolveStages;
  var _EffectChain_callOutputRect;
  var _EffectChain_buildDims;
  var _EffectChain_hostEffectDims;
  var _EffectChain_ensureIntermediate;
  var _EffectChain_canvasRectInElementLocal;
  var _EffectChain_hostFrameDims;
  var EffectChain = class {
    constructor(glCtx, quad, pixelRatio, effects, vfxProps, capture, isPostEffect, programCache) {
      _EffectChain_instances.add(this);
      _EffectChain_glCtx.set(this, void 0);
      _EffectChain_quad.set(this, void 0);
      _EffectChain_pixelRatio.set(this, void 0);
      _EffectChain_vfxProps.set(this, void 0);
      _EffectChain_programCache.set(this, void 0);
      _EffectChain_effects.set(this, void 0);
      _EffectChain_hosts.set(this, void 0);
      _EffectChain_renderingIndices.set(this, void 0);
      _EffectChain_intermediates.set(this, []);
      _EffectChain_stages.set(this, []);
      _EffectChain_capture.set(this, void 0);
      _EffectChain_warnedEffects.set(this, /* @__PURE__ */ new Set());
      _EffectChain_disposed.set(this, false);
      _EffectChain_isPostEffect.set(this, void 0);
      _EffectChain_lastHitTestPad.set(this, createMargin(0));
      _EffectChain_ownedPassthroughHost.set(this, null);
      __classPrivateFieldSet7(this, _EffectChain_glCtx, glCtx, "f");
      __classPrivateFieldSet7(this, _EffectChain_quad, quad, "f");
      __classPrivateFieldSet7(this, _EffectChain_pixelRatio, pixelRatio, "f");
      __classPrivateFieldSet7(this, _EffectChain_vfxProps, vfxProps, "f");
      __classPrivateFieldSet7(this, _EffectChain_programCache, programCache, "f");
      __classPrivateFieldSet7(this, _EffectChain_effects, effects, "f");
      __classPrivateFieldSet7(this, _EffectChain_capture, capture, "f");
      __classPrivateFieldSet7(this, _EffectChain_isPostEffect, isPostEffect, "f");
      __classPrivateFieldSet7(this, _EffectChain_hosts, effects.map(() => __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_newHost).call(this)), "f");
      if (effects.length === 0) {
        __classPrivateFieldSet7(this, _EffectChain_ownedPassthroughHost, __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_newHost).call(this), "f");
      }
      __classPrivateFieldSet7(this, _EffectChain_renderingIndices, __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_computeRenderingIndices).call(this), "f");
    }
    get effects() {
      return __classPrivateFieldGet7(this, _EffectChain_effects, "f");
    }
    get hosts() {
      return __classPrivateFieldGet7(this, _EffectChain_hosts, "f");
    }
    get renderingIndices() {
      return __classPrivateFieldGet7(this, _EffectChain_renderingIndices, "f");
    }
    /** Test-only accessor for per-stage layout data. @internal */
    get stages() {
      return __classPrivateFieldGet7(this, _EffectChain_stages, "f");
    }
    /**
     * Per-side pad in **device px** to grow the visibility hit-test
     * rect by, so glow / trail extending past the element rect keeps
     * the chain running while the padded region is on-screen. Reflects
     * the most recent rendered frame; empty / first-frame chains
     * return zero margins. Caller divides by `pixelRatio` to convert
     * to CSS px before passing to `growRect`.
     */
    get hitTestPadBuffer() {
      return __classPrivateFieldGet7(this, _EffectChain_lastHitTestPad, "f");
    }
    /**
     * Sequentially run each effect's `init`. On throw, dispose prior
     * effects in reverse order (the failing effect's own `dispose` is
     * NOT called) and rethrow.
     */
    async initAll() {
      for (let i = 0; i < __classPrivateFieldGet7(this, _EffectChain_effects, "f").length; i++) {
        const e = __classPrivateFieldGet7(this, _EffectChain_effects, "f")[i];
        const host = __classPrivateFieldGet7(this, _EffectChain_hosts, "f")[i];
        host.setPhase("init");
        try {
          if (e.init) {
            await e.init(host.ctx);
          }
        } catch (err) {
          console.error(`[VFX-JS] effect[${i}].init() failed:`, err);
          for (let j = i - 1; j >= 0; j--) {
            __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_safeDispose).call(this, j);
            __classPrivateFieldGet7(this, _EffectChain_hosts, "f")[j].dispose();
          }
          __classPrivateFieldGet7(this, _EffectChain_hosts, "f")[i].dispose();
          throw err;
        }
        host.setPhase("update");
      }
    }
    /** One frame. No-op when `!isVisible`. */
    run(input) {
      var _a;
      if (__classPrivateFieldGet7(this, _EffectChain_disposed, "f")) {
        return;
      }
      if (!input.isVisible) {
        return;
      }
      __classPrivateFieldSet7(this, _EffectChain_renderingIndices, __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_computeRenderingIndices).call(this), "f");
      const stageCount = __classPrivateFieldGet7(this, _EffectChain_renderingIndices, "f").length;
      for (const host of __classPrivateFieldGet7(this, _EffectChain_hosts, "f")) {
        host.setFrameState({
          time: input.time,
          deltaTime: input.deltaTime,
          mouse: input.mouse,
          mouseViewport: input.mouseViewport,
          intersection: input.intersection,
          enterTime: input.enterTime,
          leaveTime: input.leaveTime,
          uniforms: input.resolvedUniforms
        });
      }
      __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_resolveStages).call(this, input);
      for (let k = 0; k < __classPrivateFieldGet7(this, _EffectChain_hosts, "f").length; k++) {
        __classPrivateFieldGet7(this, _EffectChain_hosts, "f")[k].setFrameDims(__classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_hostFrameDims).call(this, k, input));
        __classPrivateFieldGet7(this, _EffectChain_hosts, "f")[k].setEffectDims(__classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_hostEffectDims).call(this, k, input));
      }
      for (let i = 0; i < __classPrivateFieldGet7(this, _EffectChain_effects, "f").length; i++) {
        const e = __classPrivateFieldGet7(this, _EffectChain_effects, "f")[i];
        if (!e.update) {
          continue;
        }
        const host = __classPrivateFieldGet7(this, _EffectChain_hosts, "f")[i];
        host.setPhase("update");
        try {
          e.update(host.ctx);
        } catch (err) {
          const key = `${i}:update`;
          if (!__classPrivateFieldGet7(this, _EffectChain_warnedEffects, "f").has(key)) {
            __classPrivateFieldGet7(this, _EffectChain_warnedEffects, "f").add(key);
            console.warn(`[VFX-JS] effect[${i}].update() threw; skipping this frame's update:`, err);
          }
        }
      }
      if (stageCount === 0) {
        const host = (_a = __classPrivateFieldGet7(this, _EffectChain_ownedPassthroughHost, "f")) != null ? _a : __classPrivateFieldGet7(this, _EffectChain_hosts, "f")[0];
        host.passthroughCopy(__classPrivateFieldGet7(this, _EffectChain_capture, "f"), input.finalTarget, input.elementRectOnCanvasPx);
        return;
      }
      for (let k = 0; k < stageCount; k++) {
        const i = __classPrivateFieldGet7(this, _EffectChain_renderingIndices, "f")[k];
        const host = __classPrivateFieldGet7(this, _EffectChain_hosts, "f")[i];
        const effect = __classPrivateFieldGet7(this, _EffectChain_effects, "f")[i];
        if (!effect.render) {
          continue;
        }
        host.setPhase("render");
        host.tickAutoUpdates();
        const srcHandle = k === 0 ? __classPrivateFieldGet7(this, _EffectChain_capture, "f") : __classPrivateFieldGet7(this, _EffectChain_intermediates, "f")[k - 1].texHandle;
        host.setSrc(srcHandle);
        let outputHandle;
        if (k === stageCount - 1) {
          outputHandle = input.finalTarget;
        } else {
          outputHandle = __classPrivateFieldGet7(this, _EffectChain_intermediates, "f")[k].rtHandle;
          host.clearRt(outputHandle);
        }
        host.setOutput(outputHandle);
        try {
          effect.render(host.ctx);
        } catch (err) {
          const key = `${i}:render`;
          if (!__classPrivateFieldGet7(this, _EffectChain_warnedEffects, "f").has(key)) {
            __classPrivateFieldGet7(this, _EffectChain_warnedEffects, "f").add(key);
            console.warn(`[VFX-JS] effect[${i}].render() threw; falling back to passthrough:`, err);
          }
          const vp = __classPrivateFieldGet7(this, _EffectChain_stages, "f")[k].outputViewport;
          if (outputHandle === null) {
            host.passthroughCopy(srcHandle, null, vp);
          } else if (k === stageCount - 1) {
            host.passthroughCopy(srcHandle, outputHandle, vp);
          } else {
            host.passthroughCopy(srcHandle, outputHandle, {
              x: 0,
              y: 0,
              w: outputHandle.width,
              h: outputHandle.height
            });
          }
        }
        host.setPhase("update");
      }
    }
    dispose() {
      if (__classPrivateFieldGet7(this, _EffectChain_disposed, "f")) {
        return;
      }
      __classPrivateFieldSet7(this, _EffectChain_disposed, true, "f");
      for (let i = __classPrivateFieldGet7(this, _EffectChain_effects, "f").length - 1; i >= 0; i--) {
        __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_safeDispose).call(this, i);
        __classPrivateFieldGet7(this, _EffectChain_hosts, "f")[i].dispose();
      }
      if (__classPrivateFieldGet7(this, _EffectChain_ownedPassthroughHost, "f")) {
        __classPrivateFieldGet7(this, _EffectChain_ownedPassthroughHost, "f").dispose();
        __classPrivateFieldSet7(this, _EffectChain_ownedPassthroughHost, null, "f");
      }
      for (const im of __classPrivateFieldGet7(this, _EffectChain_intermediates, "f")) {
        im.fb.dispose();
      }
      __classPrivateFieldSet7(this, _EffectChain_intermediates, [], "f");
      __classPrivateFieldSet7(this, _EffectChain_stages, [], "f");
    }
    /**
     * Replace the chain's effects with a new array, preserving hosts /
     * init state for effects whose reference is unchanged. Reordering
     * the same set of effects calls no `init` / `dispose`. Newly added
     * effects get a fresh host and `init`; removed effects' `dispose`
     * runs and their host is destroyed. Intermediate RTs are torn down
     * and lazily rebuilt on the next frame (sizes follow the new chain).
     *
     * On `init` failure of a newly-added effect, the freshly-created
     * hosts are rolled back and the existing chain is left intact.
     */
    async replaceEffects(newEffects) {
      if (__classPrivateFieldGet7(this, _EffectChain_disposed, "f")) {
        throw new Error("[VFX-JS] replaceEffects on disposed chain");
      }
      const oldEffects = __classPrivateFieldGet7(this, _EffectChain_effects, "f");
      const oldHosts = __classPrivateFieldGet7(this, _EffectChain_hosts, "f");
      const reusedHostByEffect = /* @__PURE__ */ new Map();
      for (let i = 0; i < oldEffects.length; i++) {
        reusedHostByEffect.set(oldEffects[i], oldHosts[i]);
      }
      const nextHosts = new Array(newEffects.length);
      const newlyCreated = [];
      for (let i = 0; i < newEffects.length; i++) {
        const e = newEffects[i];
        const reused = reusedHostByEffect.get(e);
        if (reused) {
          nextHosts[i] = reused;
          reusedHostByEffect.delete(e);
        } else {
          const host = __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_newHost).call(this);
          nextHosts[i] = host;
          newlyCreated.push({ host, effect: e });
        }
      }
      for (let i = 0; i < newlyCreated.length; i++) {
        const { host, effect } = newlyCreated[i];
        host.setPhase("init");
        try {
          if (effect.init) {
            await effect.init(host.ctx);
          }
          host.setPhase("update");
        } catch (err) {
          console.error("[VFX-JS] replaceEffects: new effect init() failed:", err);
          for (let j = i - 1; j >= 0; j--) {
            const prior = newlyCreated[j];
            if (prior.effect.dispose) {
              try {
                prior.effect.dispose();
              } catch (e2) {
                console.error("[VFX-JS] dispose during init rollback threw:", e2);
              }
            }
            prior.host.dispose();
          }
          host.dispose();
          throw err;
        }
      }
      for (const [effect, host] of reusedHostByEffect) {
        if (effect.dispose) {
          try {
            effect.dispose();
          } catch (err) {
            console.error("[VFX-JS] effect.dispose() threw during replaceEffects:", err);
          }
        }
        host.dispose();
      }
      for (const im of __classPrivateFieldGet7(this, _EffectChain_intermediates, "f")) {
        im.fb.dispose();
      }
      __classPrivateFieldSet7(this, _EffectChain_intermediates, [], "f");
      __classPrivateFieldSet7(this, _EffectChain_stages, [], "f");
      if (newEffects.length === 0 && !__classPrivateFieldGet7(this, _EffectChain_ownedPassthroughHost, "f")) {
        __classPrivateFieldSet7(this, _EffectChain_ownedPassthroughHost, __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_newHost).call(this), "f");
      } else if (newEffects.length > 0 && __classPrivateFieldGet7(this, _EffectChain_ownedPassthroughHost, "f")) {
        __classPrivateFieldGet7(this, _EffectChain_ownedPassthroughHost, "f").dispose();
        __classPrivateFieldSet7(this, _EffectChain_ownedPassthroughHost, null, "f");
      }
      __classPrivateFieldSet7(this, _EffectChain_effects, newEffects, "f");
      __classPrivateFieldSet7(this, _EffectChain_hosts, nextHosts, "f");
      __classPrivateFieldSet7(this, _EffectChain_renderingIndices, __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_computeRenderingIndices).call(this), "f");
      __classPrivateFieldGet7(this, _EffectChain_warnedEffects, "f").clear();
    }
  };
  _EffectChain_glCtx = /* @__PURE__ */ new WeakMap(), _EffectChain_quad = /* @__PURE__ */ new WeakMap(), _EffectChain_pixelRatio = /* @__PURE__ */ new WeakMap(), _EffectChain_vfxProps = /* @__PURE__ */ new WeakMap(), _EffectChain_programCache = /* @__PURE__ */ new WeakMap(), _EffectChain_effects = /* @__PURE__ */ new WeakMap(), _EffectChain_hosts = /* @__PURE__ */ new WeakMap(), _EffectChain_renderingIndices = /* @__PURE__ */ new WeakMap(), _EffectChain_intermediates = /* @__PURE__ */ new WeakMap(), _EffectChain_stages = /* @__PURE__ */ new WeakMap(), _EffectChain_capture = /* @__PURE__ */ new WeakMap(), _EffectChain_warnedEffects = /* @__PURE__ */ new WeakMap(), _EffectChain_disposed = /* @__PURE__ */ new WeakMap(), _EffectChain_isPostEffect = /* @__PURE__ */ new WeakMap(), _EffectChain_lastHitTestPad = /* @__PURE__ */ new WeakMap(), _EffectChain_ownedPassthroughHost = /* @__PURE__ */ new WeakMap(), _EffectChain_instances = /* @__PURE__ */ new WeakSet(), _EffectChain_computeRenderingIndices = function _EffectChain_computeRenderingIndices2() {
    return __classPrivateFieldGet7(this, _EffectChain_effects, "f").map((e, i) => typeof e.render === "function" && e.enabled !== false ? i : -1).filter((i) => i >= 0);
  }, _EffectChain_newHost = function _EffectChain_newHost2() {
    return new EffectHost(__classPrivateFieldGet7(this, _EffectChain_glCtx, "f"), __classPrivateFieldGet7(this, _EffectChain_quad, "f"), __classPrivateFieldGet7(this, _EffectChain_pixelRatio, "f"), __classPrivateFieldGet7(this, _EffectChain_capture, "f"), __classPrivateFieldGet7(this, _EffectChain_vfxProps, "f"), __classPrivateFieldGet7(this, _EffectChain_programCache, "f"));
  }, _EffectChain_safeDispose = function _EffectChain_safeDispose2(i) {
    const e = __classPrivateFieldGet7(this, _EffectChain_effects, "f")[i];
    if (!e.dispose) {
      return;
    }
    try {
      e.dispose();
    } catch (err) {
      console.error(`[VFX-JS] effect[${i}].dispose() threw:`, err);
    }
  }, _EffectChain_resolveStages = function _EffectChain_resolveStages2(input) {
    const stageCount = __classPrivateFieldGet7(this, _EffectChain_renderingIndices, "f").length;
    __classPrivateFieldSet7(this, _EffectChain_stages, new Array(stageCount), "f");
    if (stageCount === 0) {
      return;
    }
    const elementPixel = __classPrivateFieldGet7(this, _EffectChain_isPostEffect, "f") ? input.canvasBufferSize : input.elementBufferSize;
    const contentRect = [
      0,
      0,
      elementPixel[0],
      elementPixel[1]
    ];
    const canvasRect = __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_canvasRectInElementLocal).call(this, input);
    let srcRect = contentRect;
    for (let k = 0; k < stageCount; k++) {
      const i = __classPrivateFieldGet7(this, _EffectChain_renderingIndices, "f")[k];
      const effect = __classPrivateFieldGet7(this, _EffectChain_effects, "f")[i];
      const isLast = k === stageCount - 1;
      const resolved = __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_callOutputRect).call(this, effect, srcRect, contentRect, canvasRect, input);
      const dstRect = resolved != null ? resolved : srcRect;
      const dstBufferSize = [dstRect[2], dstRect[3]];
      const contentRectUv = rectInRect(contentRect, dstRect);
      const outputViewport = isLast ? {
        x: input.elementRectOnCanvasPx.x + dstRect[0],
        y: input.elementRectOnCanvasPx.y + dstRect[1],
        w: dstBufferSize[0],
        h: dstBufferSize[1]
      } : { x: 0, y: 0, w: dstBufferSize[0], h: dstBufferSize[1] };
      __classPrivateFieldGet7(this, _EffectChain_stages, "f")[k] = {
        dstRect,
        dstBufferSize,
        contentRectUv,
        outputViewport
      };
      if (!isLast) {
        __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_ensureIntermediate).call(this, k, dstBufferSize);
      }
      srcRect = dstRect;
    }
    const [lx, ly, lw, lh] = __classPrivateFieldGet7(this, _EffectChain_stages, "f")[stageCount - 1].dstRect;
    __classPrivateFieldSet7(this, _EffectChain_lastHitTestPad, createMargin({
      top: Math.max(0, ly + lh - elementPixel[1]),
      right: Math.max(0, lx + lw - elementPixel[0]),
      bottom: Math.max(0, -ly),
      left: Math.max(0, -lx)
    }), "f");
  }, _EffectChain_callOutputRect = function _EffectChain_callOutputRect2(effect, srcRect, contentRect, canvasRect, input) {
    if (!effect.outputRect) {
      return void 0;
    }
    return effect.outputRect(__classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_buildDims).call(this, input, contentRect, srcRect, canvasRect));
  }, _EffectChain_buildDims = function _EffectChain_buildDims2(input, contentRect, srcRect, canvasRect) {
    const pixelRatio = input.canvasBufferSize[0] / input.canvasSize[0] || 1;
    return {
      element: __classPrivateFieldGet7(this, _EffectChain_isPostEffect, "f") ? input.canvasSize : input.elementSize,
      elementPixel: __classPrivateFieldGet7(this, _EffectChain_isPostEffect, "f") ? input.canvasBufferSize : input.elementBufferSize,
      canvas: input.canvasSize,
      canvasPixel: input.canvasBufferSize,
      pixelRatio,
      contentRect,
      srcRect,
      canvasRect
    };
  }, _EffectChain_hostEffectDims = function _EffectChain_hostEffectDims2(k, input) {
    const elementPixel = __classPrivateFieldGet7(this, _EffectChain_isPostEffect, "f") ? input.canvasBufferSize : input.elementBufferSize;
    const contentRect = [
      0,
      0,
      elementPixel[0],
      elementPixel[1]
    ];
    const canvasRect = __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_canvasRectInElementLocal).call(this, input);
    const renderPos = __classPrivateFieldGet7(this, _EffectChain_renderingIndices, "f").indexOf(k);
    const srcRect = renderPos <= 0 ? contentRect : __classPrivateFieldGet7(this, _EffectChain_stages, "f")[renderPos - 1].dstRect;
    return __classPrivateFieldGet7(this, _EffectChain_instances, "m", _EffectChain_buildDims).call(this, input, contentRect, srcRect, canvasRect);
  }, _EffectChain_ensureIntermediate = function _EffectChain_ensureIntermediate2(k, bufferSize) {
    const current = __classPrivateFieldGet7(this, _EffectChain_intermediates, "f")[k];
    if (current && current.fb.width === bufferSize[0] && current.fb.height === bufferSize[1]) {
      return;
    }
    if (current) {
      current.fb.dispose();
    }
    const fb = new Framebuffer(__classPrivateFieldGet7(this, _EffectChain_glCtx, "f"), bufferSize[0], bufferSize[1]);
    const rtHandle = makeEffectRenderTargetFromFb(fb);
    const texHandle = makeEffectTexture(() => fb.texture, () => fb.width, () => fb.height);
    __classPrivateFieldGet7(this, _EffectChain_intermediates, "f")[k] = {
      fb,
      rtHandle,
      texHandle,
      bufferSize
    };
  }, _EffectChain_canvasRectInElementLocal = function _EffectChain_canvasRectInElementLocal2(input) {
    const [cw, ch] = input.canvasBufferSize;
    if (__classPrivateFieldGet7(this, _EffectChain_isPostEffect, "f")) {
      return [0, 0, cw, ch];
    }
    const { x, y } = input.elementRectOnCanvasPx;
    return [-x, -y, cw, ch];
  }, _EffectChain_hostFrameDims = function _EffectChain_hostFrameDims2(k, input) {
    const renderPos = __classPrivateFieldGet7(this, _EffectChain_renderingIndices, "f").indexOf(k);
    let outputW;
    let outputH;
    let outputViewport;
    let contentRectUv;
    let srcRectUv;
    if (renderPos < 0) {
      outputW = input.elementBufferSize[0];
      outputH = input.elementBufferSize[1];
      outputViewport = { x: 0, y: 0, w: outputW, h: outputH };
      contentRectUv = [0, 0, 1, 1];
      srcRectUv = [0, 0, 1, 1];
    } else {
      const stage = __classPrivateFieldGet7(this, _EffectChain_stages, "f")[renderPos];
      outputW = stage.dstBufferSize[0];
      outputH = stage.dstBufferSize[1];
      outputViewport = stage.outputViewport;
      contentRectUv = stage.contentRectUv;
      srcRectUv = renderPos === 0 ? [0, 0, 1, 1] : __classPrivateFieldGet7(this, _EffectChain_stages, "f")[renderPos - 1].contentRectUv;
    }
    return {
      outputBufferW: outputW,
      outputBufferH: outputH,
      canvasBufferSize: input.canvasBufferSize,
      outputViewport,
      elementBufferW: input.elementBufferSize[0],
      elementBufferH: input.elementBufferSize[1],
      contentRectUv,
      srcRectUv
    };
  };

  // node_modules/@vfx-js/core/lib/esm/gifuct-js/bytestream.js
  function ByteStream(data) {
    this.data = data;
    this.pos = 0;
  }
  ByteStream.prototype.readByte = function() {
    return this.data[this.pos++];
  };
  ByteStream.prototype.peekByte = function() {
    return this.data[this.pos];
  };
  ByteStream.prototype.readBytes = function(n) {
    return this.data.subarray(this.pos, this.pos += n);
  };
  ByteStream.prototype.peekBytes = function(n) {
    return this.data.subarray(this.pos, this.pos + n);
  };
  ByteStream.prototype.readString = function(len) {
    var str = "";
    for (var i = 0; i < len; i++) {
      str += String.fromCharCode(this.readByte());
    }
    return str;
  };
  ByteStream.prototype.readBitArray = function() {
    var arr = [];
    var bite = this.readByte();
    for (var i = 7; i >= 0; i--) {
      arr.push(!!(bite & 1 << i));
    }
    return arr;
  };
  ByteStream.prototype.readUnsigned = function(littleEndian) {
    var a = this.readBytes(2);
    if (littleEndian) {
      return (a[1] << 8) + a[0];
    } else {
      return (a[0] << 8) + a[1];
    }
  };
  var bytestream_default = ByteStream;

  // node_modules/@vfx-js/core/lib/esm/gifuct-js/dataparser.js
  function DataParser(data) {
    this.stream = new bytestream_default(data);
    this.output = {};
  }
  DataParser.prototype.parse = function(schema) {
    this.parseParts(this.output, schema);
    return this.output;
  };
  DataParser.prototype.parseParts = function(obj, schema) {
    for (var i = 0; i < schema.length; i++) {
      var part = schema[i];
      this.parsePart(obj, part);
    }
  };
  DataParser.prototype.parsePart = function(obj, part) {
    var name = part.label;
    var value;
    if (part.requires && !part.requires(this.stream, this.output, obj)) {
      return;
    }
    if (part.loop) {
      var items = [];
      while (part.loop(this.stream)) {
        var item = {};
        this.parseParts(item, part.parts);
        items.push(item);
      }
      obj[name] = items;
    } else if (part.parts) {
      value = {};
      this.parseParts(value, part.parts);
      obj[name] = value;
    } else if (part.parser) {
      value = part.parser(this.stream, this.output, obj);
      if (!part.skip) {
        obj[name] = value;
      }
    } else if (part.bits) {
      obj[name] = this.parseBits(part.bits);
    }
  };
  function bitsToNum(bitArray) {
    return bitArray.reduce(function(s, n) {
      return s * 2 + n;
    }, 0);
  }
  DataParser.prototype.parseBits = function(details) {
    var out = {};
    var bits = this.stream.readBitArray();
    for (var key in details) {
      var item = details[key];
      if (item.length) {
        out[key] = bitsToNum(bits.slice(item.index, item.index + item.length));
      } else {
        out[key] = bits[item.index];
      }
    }
    return out;
  };
  var dataparser_default = DataParser;

  // node_modules/@vfx-js/core/lib/esm/gifuct-js/parsers.js
  var Parsers = {
    // read a byte
    readByte: function() {
      return function(stream) {
        return stream.readByte();
      };
    },
    // read an array of bytes
    readBytes: function(length) {
      return function(stream) {
        return stream.readBytes(length);
      };
    },
    // read a string from bytes
    readString: function(length) {
      return function(stream) {
        return stream.readString(length);
      };
    },
    // read an unsigned int (with endian)
    readUnsigned: function(littleEndian) {
      return function(stream) {
        return stream.readUnsigned(littleEndian);
      };
    },
    // read an array of byte sets
    readArray: function(size, countFunc) {
      return function(stream, obj, parent) {
        var count = countFunc(stream, obj, parent);
        var arr = new Array(count);
        for (var i = 0; i < count; i++) {
          arr[i] = stream.readBytes(size);
        }
        return arr;
      };
    }
  };
  var parsers_default = Parsers;

  // node_modules/@vfx-js/core/lib/esm/gifuct-js/schema.js
  var subBlocks = {
    label: "blocks",
    parser: function(stream) {
      var views = [];
      var total = 0;
      var terminator = 0;
      for (var size = stream.readByte(); size !== terminator; size = stream.readByte()) {
        views.push(stream.readBytes(size));
        total += size;
      }
      var out = new Uint8Array(total);
      total = 0;
      for (var i = 0; i < views.length; i++) {
        out.set(views[i], total);
        total += views[i].length;
      }
      return out;
    }
  };
  var gce = {
    label: "gce",
    requires: function(stream) {
      var codes = stream.peekBytes(2);
      return codes[0] === 33 && codes[1] === 249;
    },
    parts: [
      { label: "codes", parser: parsers_default.readBytes(2), skip: true },
      { label: "byteSize", parser: parsers_default.readByte() },
      {
        label: "extras",
        bits: {
          future: { index: 0, length: 3 },
          disposal: { index: 3, length: 3 },
          userInput: { index: 6 },
          transparentColorGiven: { index: 7 }
        }
      },
      { label: "delay", parser: parsers_default.readUnsigned(true) },
      { label: "transparentColorIndex", parser: parsers_default.readByte() },
      { label: "terminator", parser: parsers_default.readByte(), skip: true }
    ]
  };
  var image = {
    label: "image",
    requires: function(stream) {
      var code = stream.peekByte();
      return code === 44;
    },
    parts: [
      { label: "code", parser: parsers_default.readByte(), skip: true },
      {
        label: "descriptor",
        // image descriptor
        parts: [
          { label: "left", parser: parsers_default.readUnsigned(true) },
          { label: "top", parser: parsers_default.readUnsigned(true) },
          { label: "width", parser: parsers_default.readUnsigned(true) },
          { label: "height", parser: parsers_default.readUnsigned(true) },
          {
            label: "lct",
            bits: {
              exists: { index: 0 },
              interlaced: { index: 1 },
              sort: { index: 2 },
              future: { index: 3, length: 2 },
              size: { index: 5, length: 3 }
            }
          }
        ]
      },
      {
        label: "lct",
        // optional local color table
        requires: function(stream, obj, parent) {
          return parent.descriptor.lct.exists;
        },
        parser: parsers_default.readArray(3, function(stream, obj, parent) {
          return Math.pow(2, parent.descriptor.lct.size + 1);
        })
      },
      {
        label: "data",
        // the image data blocks
        parts: [
          { label: "minCodeSize", parser: parsers_default.readByte() },
          subBlocks
        ]
      }
    ]
  };
  var text = {
    label: "text",
    requires: function(stream) {
      var codes = stream.peekBytes(2);
      return codes[0] === 33 && codes[1] === 1;
    },
    parts: [
      { label: "codes", parser: parsers_default.readBytes(2), skip: true },
      { label: "blockSize", parser: parsers_default.readByte() },
      {
        label: "preData",
        parser: function(stream, obj, parent) {
          return stream.readBytes(parent.text.blockSize);
        }
      },
      subBlocks
    ]
  };
  var application = {
    label: "application",
    requires: function(stream, obj, parent) {
      var codes = stream.peekBytes(2);
      return codes[0] === 33 && codes[1] === 255;
    },
    parts: [
      { label: "codes", parser: parsers_default.readBytes(2), skip: true },
      { label: "blockSize", parser: parsers_default.readByte() },
      {
        label: "id",
        parser: function(stream, obj, parent) {
          return stream.readString(parent.blockSize);
        }
      },
      subBlocks
    ]
  };
  var comment = {
    label: "comment",
    requires: function(stream, obj, parent) {
      var codes = stream.peekBytes(2);
      return codes[0] === 33 && codes[1] === 254;
    },
    parts: [
      { label: "codes", parser: parsers_default.readBytes(2), skip: true },
      subBlocks
    ]
  };
  var frames = {
    label: "frames",
    parts: [gce, application, comment, image, text],
    loop: function(stream) {
      var nextCode = stream.peekByte();
      return nextCode === 33 || nextCode === 44;
    }
  };
  var schemaGIF = [
    {
      label: "header",
      // gif header
      parts: [
        { label: "signature", parser: parsers_default.readString(3) },
        { label: "version", parser: parsers_default.readString(3) }
      ]
    },
    {
      label: "lsd",
      // local screen descriptor
      parts: [
        { label: "width", parser: parsers_default.readUnsigned(true) },
        { label: "height", parser: parsers_default.readUnsigned(true) },
        {
          label: "gct",
          bits: {
            exists: { index: 0 },
            resolution: { index: 1, length: 3 },
            sort: { index: 4 },
            size: { index: 5, length: 3 }
          }
        },
        { label: "backgroundColorIndex", parser: parsers_default.readByte() },
        { label: "pixelAspectRatio", parser: parsers_default.readByte() }
      ]
    },
    {
      label: "gct",
      // global color table
      requires: function(stream, obj) {
        return obj.lsd.gct.exists;
      },
      parser: parsers_default.readArray(3, function(stream, obj) {
        return Math.pow(2, obj.lsd.gct.size + 1);
      })
    },
    frames
    // content frames
  ];
  var schema_default = schemaGIF;

  // node_modules/@vfx-js/core/lib/esm/gifuct-js/gif.js
  function GIF(arrayBuffer) {
    var byteData = new Uint8Array(arrayBuffer);
    var parser = new dataparser_default(byteData);
    this.raw = parser.parse(schema_default);
    this.raw.hasImages = false;
    for (var f = 0; f < this.raw.frames.length; f++) {
      if (this.raw.frames[f].image) {
        this.raw.hasImages = true;
        break;
      }
    }
  }
  GIF.prototype.decompressFrame = function(index, buildPatch) {
    if (index >= this.raw.frames.length) {
      return null;
    }
    var frame = this.raw.frames[index];
    if (frame.image) {
      var totalPixels = frame.image.descriptor.width * frame.image.descriptor.height;
      var pixels = lzw(frame.image.data.minCodeSize, frame.image.data.blocks, totalPixels);
      if (frame.image.descriptor.lct.interlaced) {
        pixels = deinterlace(pixels, frame.image.descriptor.width);
      }
      var image2 = {
        pixels,
        dims: {
          top: frame.image.descriptor.top,
          left: frame.image.descriptor.left,
          width: frame.image.descriptor.width,
          height: frame.image.descriptor.height
        }
      };
      if (frame.image.descriptor.lct && frame.image.descriptor.lct.exists) {
        image2.colorTable = frame.image.lct;
      } else {
        image2.colorTable = this.raw.gct;
      }
      if (frame.gce) {
        image2.delay = (frame.gce.delay || 10) * 10;
        image2.disposalType = frame.gce.extras.disposal;
        if (frame.gce.extras.transparentColorGiven) {
          image2.transparentIndex = frame.gce.transparentColorIndex;
        }
      }
      if (buildPatch) {
        image2.patch = generatePatch(image2);
      }
      return image2;
    }
    return null;
    function lzw(minCodeSize, data, pixelCount) {
      var MAX_STACK_SIZE = 4096;
      var nullCode = -1;
      var npix = pixelCount;
      var available, clear, code_mask, code_size, count, end_of_information, in_code, old_code, bits, code, i, datum, data_size, first, top, bi, pi;
      var dstPixels = new Array(pixelCount);
      var prefix = new Array(MAX_STACK_SIZE);
      var suffix = new Array(MAX_STACK_SIZE);
      var pixelStack = new Array(MAX_STACK_SIZE + 1);
      data_size = minCodeSize;
      clear = 1 << data_size;
      end_of_information = clear + 1;
      available = clear + 2;
      old_code = nullCode;
      code_size = data_size + 1;
      code_mask = (1 << code_size) - 1;
      for (code = 0; code < clear; code++) {
        prefix[code] = 0;
        suffix[code] = code;
      }
      datum = bits = count = first = top = pi = bi = 0;
      for (i = 0; i < npix; ) {
        if (top === 0) {
          if (bits < code_size) {
            datum += data[bi] << bits;
            bits += 8;
            bi++;
            continue;
          }
          code = datum & code_mask;
          datum >>= code_size;
          bits -= code_size;
          if (code > available || code == end_of_information) {
            break;
          }
          if (code == clear) {
            code_size = data_size + 1;
            code_mask = (1 << code_size) - 1;
            available = clear + 2;
            old_code = nullCode;
            continue;
          }
          if (old_code == nullCode) {
            pixelStack[top++] = suffix[code];
            old_code = code;
            first = code;
            continue;
          }
          in_code = code;
          if (code == available) {
            pixelStack[top++] = first;
            code = old_code;
          }
          while (code > clear) {
            pixelStack[top++] = suffix[code];
            code = prefix[code];
          }
          first = suffix[code] & 255;
          pixelStack[top++] = first;
          if (available < MAX_STACK_SIZE) {
            prefix[available] = old_code;
            suffix[available] = first;
            available++;
            if ((available & code_mask) === 0 && available < MAX_STACK_SIZE) {
              code_size++;
              code_mask += available;
            }
          }
          old_code = in_code;
        }
        top--;
        dstPixels[pi++] = pixelStack[top];
        i++;
      }
      for (i = pi; i < npix; i++) {
        dstPixels[i] = 0;
      }
      return dstPixels;
    }
    function deinterlace(pixels2, width) {
      var newPixels = new Array(pixels2.length);
      var rows = pixels2.length / width;
      var cpRow = function(toRow2, fromRow2) {
        var fromPixels = pixels2.slice(fromRow2 * width, (fromRow2 + 1) * width);
        newPixels.splice.apply(newPixels, [toRow2 * width, width].concat(fromPixels));
      };
      var offsets = [0, 4, 2, 1];
      var steps = [8, 8, 4, 2];
      var fromRow = 0;
      for (var pass = 0; pass < 4; pass++) {
        for (var toRow = offsets[pass]; toRow < rows; toRow += steps[pass]) {
          cpRow(toRow, fromRow);
          fromRow++;
        }
      }
      return newPixels;
    }
    function generatePatch(image3) {
      var totalPixels2 = image3.pixels.length;
      var patchData = new Uint8ClampedArray(totalPixels2 * 4);
      for (var i = 0; i < totalPixels2; i++) {
        var pos = i * 4;
        var colorIndex = image3.pixels[i];
        var color = image3.colorTable[colorIndex];
        patchData[pos] = color[0];
        patchData[pos + 1] = color[1];
        patchData[pos + 2] = color[2];
        patchData[pos + 3] = colorIndex !== image3.transparentIndex ? 255 : 0;
      }
      return patchData;
    }
  };
  GIF.prototype.decompressFrames = function(buildPatch, startFrame, endFrame) {
    if (startFrame === void 0) {
      startFrame = 0;
    }
    if (endFrame === void 0) {
      endFrame = this.raw.frames.length;
    } else {
      endFrame = Math.min(endFrame, this.raw.frames.length);
    }
    var frames2 = [];
    for (var i = startFrame; i < endFrame; i++) {
      var frame = this.raw.frames[i];
      if (frame.image) {
        frames2.push(this.decompressFrame(i, buildPatch));
      }
    }
    return frames2;
  };
  var gif_default = GIF;

  // node_modules/@vfx-js/core/lib/esm/gifuct-js/index.js
  var gifuct_js_default = gif_default;

  // node_modules/@vfx-js/core/lib/esm/gif.js
  var GIFData = class _GIFData {
    static async create(src, pixelRatio) {
      const gif = await fetch(src).then((resp) => resp.arrayBuffer()).then((buff) => new gifuct_js_default(buff));
      const frames2 = gif.decompressFrames(true, void 0, void 0);
      const { width, height } = gif.raw.lsd;
      return new _GIFData(frames2, width, height, pixelRatio);
    }
    constructor(frames2, width, height, pixelRatio) {
      this.frames = [];
      this.index = 0;
      this.playTime = 0;
      this.frames = frames2;
      this.canvas = document.createElement("canvas");
      this.ctx = this.canvas.getContext("2d");
      this.pixelRatio = pixelRatio;
      this.canvas.width = width;
      this.canvas.height = height;
      this.startTime = Date.now();
    }
    getCanvas() {
      return this.canvas;
    }
    update() {
      const now = Date.now();
      const elapsedTime = now - this.startTime;
      while (this.playTime < elapsedTime) {
        const f = this.frames[this.index % this.frames.length];
        this.playTime += f.delay;
        this.index++;
      }
      const frame = this.frames[this.index % this.frames.length];
      const image2 = new ImageData(frame.patch, frame.dims.width, frame.dims.height);
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.ctx.putImageData(image2, frame.dims.left, frame.dims.top);
    }
  };

  // node_modules/@vfx-js/core/lib/esm/gl/context.js
  var __classPrivateFieldGet8 = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _GLContext_resources;
  var _GLContext_onLost;
  var _GLContext_onRestored;
  var _GLContext_handleLost;
  var _GLContext_handleRestored;
  var GLContext = class {
    constructor(canvas) {
      this.isContextLost = false;
      _GLContext_resources.set(this, /* @__PURE__ */ new Set());
      _GLContext_onLost.set(this, /* @__PURE__ */ new Set());
      _GLContext_onRestored.set(this, /* @__PURE__ */ new Set());
      _GLContext_handleLost.set(this, (event) => {
        event.preventDefault();
        this.isContextLost = true;
        for (const cb of __classPrivateFieldGet8(this, _GLContext_onLost, "f")) {
          cb();
        }
      });
      _GLContext_handleRestored.set(this, () => {
        this.isContextLost = false;
        const gl2 = this.gl;
        gl2.getExtension("EXT_color_buffer_float");
        gl2.getExtension("EXT_color_buffer_half_float");
        for (const r of __classPrivateFieldGet8(this, _GLContext_resources, "f")) {
          r.restore();
        }
        for (const cb of __classPrivateFieldGet8(this, _GLContext_onRestored, "f")) {
          cb();
        }
      });
      const gl = canvas.getContext("webgl2", {
        alpha: true,
        premultipliedAlpha: true,
        antialias: false,
        depth: false,
        stencil: false,
        preserveDrawingBuffer: false
      });
      if (!gl) {
        throw new Error("[VFX-JS] WebGL2 is not available.");
      }
      this.gl = gl;
      this.canvas = canvas;
      gl.getExtension("EXT_color_buffer_float");
      gl.getExtension("EXT_color_buffer_half_float");
      this.floatLinearFilter = !!gl.getExtension("OES_texture_float_linear");
      this.maxTextureSize = gl.getParameter(gl.MAX_TEXTURE_SIZE);
      canvas.addEventListener("webglcontextlost", __classPrivateFieldGet8(this, _GLContext_handleLost, "f"), false);
      canvas.addEventListener("webglcontextrestored", __classPrivateFieldGet8(this, _GLContext_handleRestored, "f"), false);
    }
    setSize(width, height, pixelRatio) {
      const w = Math.floor(width * pixelRatio);
      const h = Math.floor(height * pixelRatio);
      if (this.canvas.width !== w || this.canvas.height !== h) {
        this.canvas.width = w;
        this.canvas.height = h;
      }
    }
    addResource(r) {
      __classPrivateFieldGet8(this, _GLContext_resources, "f").add(r);
    }
    removeResource(r) {
      __classPrivateFieldGet8(this, _GLContext_resources, "f").delete(r);
    }
    /** Subscribe to context-lost events. Returns an unsubscribe function. */
    onContextLost(cb) {
      __classPrivateFieldGet8(this, _GLContext_onLost, "f").add(cb);
      return () => __classPrivateFieldGet8(this, _GLContext_onLost, "f").delete(cb);
    }
    /** Subscribe to context-restored events. Returns an unsubscribe function. */
    onContextRestored(cb) {
      __classPrivateFieldGet8(this, _GLContext_onRestored, "f").add(cb);
      return () => __classPrivateFieldGet8(this, _GLContext_onRestored, "f").delete(cb);
    }
  };
  _GLContext_resources = /* @__PURE__ */ new WeakMap(), _GLContext_onLost = /* @__PURE__ */ new WeakMap(), _GLContext_onRestored = /* @__PURE__ */ new WeakMap(), _GLContext_handleLost = /* @__PURE__ */ new WeakMap(), _GLContext_handleRestored = /* @__PURE__ */ new WeakMap();

  // node_modules/@vfx-js/core/lib/esm/gl/quad.js
  var __classPrivateFieldSet8 = function(receiver, state2, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state2.set(receiver, value), value;
  };
  var __classPrivateFieldGet9 = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _Quad_instances;
  var _Quad_ctx;
  var _Quad_buffer;
  var _Quad_allocate;
  var Quad = class {
    constructor(ctx) {
      _Quad_instances.add(this);
      _Quad_ctx.set(this, void 0);
      _Quad_buffer.set(this, void 0);
      __classPrivateFieldSet8(this, _Quad_ctx, ctx, "f");
      this.gl = ctx.gl;
      __classPrivateFieldGet9(this, _Quad_instances, "m", _Quad_allocate).call(this);
      ctx.addResource(this);
    }
    restore() {
      __classPrivateFieldGet9(this, _Quad_instances, "m", _Quad_allocate).call(this);
    }
    draw() {
      const gl = this.gl;
      gl.bindVertexArray(this.vao);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
    }
    dispose() {
      __classPrivateFieldGet9(this, _Quad_ctx, "f").removeResource(this);
      this.gl.deleteVertexArray(this.vao);
      this.gl.deleteBuffer(__classPrivateFieldGet9(this, _Quad_buffer, "f"));
    }
  };
  _Quad_ctx = /* @__PURE__ */ new WeakMap(), _Quad_buffer = /* @__PURE__ */ new WeakMap(), _Quad_instances = /* @__PURE__ */ new WeakSet(), _Quad_allocate = function _Quad_allocate2() {
    const gl = this.gl;
    const vao = gl.createVertexArray();
    const buffer = gl.createBuffer();
    if (!vao || !buffer) {
      throw new Error("[VFX-JS] Failed to create quad VAO");
    }
    this.vao = vao;
    __classPrivateFieldSet8(this, _Quad_buffer, buffer, "f");
    const verts = new Float32Array([
      -1,
      -1,
      0,
      1,
      -1,
      0,
      -1,
      1,
      0,
      -1,
      1,
      0,
      1,
      -1,
      0,
      1,
      1,
      0
    ]);
    gl.bindVertexArray(vao);
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(gl.ARRAY_BUFFER, verts, gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);
    gl.bindVertexArray(null);
    gl.bindBuffer(gl.ARRAY_BUFFER, null);
  };

  // node_modules/@vfx-js/core/lib/esm/render-target.js
  function createRenderTarget(ctx, width, height, opts = {}) {
    var _a;
    return new Framebuffer(ctx, width, height, { float: (_a = opts.float) != null ? _a : false });
  }
  function createPassMaterial(ctx, opts) {
    var _a, _b, _c;
    const renderingToBuffer = (_a = opts.renderingToBuffer) != null ? _a : false;
    let blend;
    if (renderingToBuffer) {
      blend = "none";
    } else if (opts.premultipliedAlpha) {
      blend = "premultiplied";
    } else {
      blend = "normal";
    }
    const glslVersion = (_b = opts.glslVersion) != null ? _b : detectGlslVersion(opts.fragmentShader);
    const vertexShader = (_c = opts.vertexShader) != null ? _c : glslVersion === "100" ? DEFAULT_VERTEX_SHADER_100 : DEFAULT_VERTEX_SHADER;
    return new Pass(ctx, vertexShader, opts.fragmentShader, opts.uniforms, blend, glslVersion);
  }

  // node_modules/@vfx-js/core/lib/esm/post-effect-pass.js
  var __classPrivateFieldSet9 = function(receiver, state2, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state2.set(receiver, value), value;
  };
  var __classPrivateFieldGet10 = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _PostEffectPass_uniforms;
  var _PostEffectPass_uniformGenerators;
  var _PostEffectPass_backbuffer;
  var _PostEffectPass_persistent;
  var _PostEffectPass_float;
  var _PostEffectPass_size;
  var PostEffectPass = class {
    constructor(ctx, fragmentShader, uniforms, persistent, float, size, hasBufferTarget, glslVersion) {
      _PostEffectPass_uniforms.set(this, void 0);
      _PostEffectPass_uniformGenerators.set(this, void 0);
      _PostEffectPass_backbuffer.set(this, void 0);
      _PostEffectPass_persistent.set(this, void 0);
      _PostEffectPass_float.set(this, void 0);
      _PostEffectPass_size.set(this, void 0);
      __classPrivateFieldSet9(this, _PostEffectPass_persistent, persistent != null ? persistent : false, "f");
      __classPrivateFieldSet9(this, _PostEffectPass_float, float != null ? float : false, "f");
      __classPrivateFieldSet9(this, _PostEffectPass_size, size, "f");
      __classPrivateFieldSet9(this, _PostEffectPass_uniformGenerators, {}, "f");
      __classPrivateFieldSet9(this, _PostEffectPass_uniforms, {
        src: { value: null },
        offset: { value: new Vec2() },
        resolution: { value: new Vec2() },
        viewport: { value: new Vec4() },
        time: { value: 0 },
        mouse: { value: new Vec2() },
        passIndex: { value: 0 }
      }, "f");
      if (uniforms) {
        for (const [key, value] of Object.entries(uniforms)) {
          if (typeof value === "function") {
            __classPrivateFieldGet10(this, _PostEffectPass_uniformGenerators, "f")[key] = value;
            __classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f")[key] = { value: value() };
          } else {
            __classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f")[key] = { value };
          }
        }
      }
      this.pass = createPassMaterial(ctx, {
        fragmentShader,
        uniforms: __classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f"),
        renderingToBuffer: hasBufferTarget != null ? hasBufferTarget : false,
        premultipliedAlpha: true,
        glslVersion
      });
    }
    get uniforms() {
      return __classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f");
    }
    setUniforms(tex, pixelRatio, xywh, time, mouseX, mouseY) {
      __classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f").src.value = tex;
      __classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f").resolution.value.set(xywh.w * pixelRatio, xywh.h * pixelRatio);
      __classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f").offset.value.set(xywh.x * pixelRatio, xywh.y * pixelRatio);
      __classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f").time.value = time;
      __classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f").mouse.value.set(mouseX * pixelRatio, mouseY * pixelRatio);
    }
    updateCustomUniforms(uniformGenerators) {
      for (const [key, generator] of Object.entries(__classPrivateFieldGet10(this, _PostEffectPass_uniformGenerators, "f"))) {
        if (__classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f")[key]) {
          __classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f")[key].value = generator();
        }
      }
      if (uniformGenerators) {
        for (const [key, generator] of Object.entries(uniformGenerators)) {
          if (__classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f")[key]) {
            __classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f")[key].value = generator();
          }
        }
      }
    }
    initializeBackbuffer(ctx, width, height, pixelRatio) {
      if (__classPrivateFieldGet10(this, _PostEffectPass_persistent, "f") && !__classPrivateFieldGet10(this, _PostEffectPass_backbuffer, "f")) {
        if (__classPrivateFieldGet10(this, _PostEffectPass_size, "f")) {
          __classPrivateFieldSet9(this, _PostEffectPass_backbuffer, new Backbuffer(ctx, __classPrivateFieldGet10(this, _PostEffectPass_size, "f")[0], __classPrivateFieldGet10(this, _PostEffectPass_size, "f")[1], 1, __classPrivateFieldGet10(this, _PostEffectPass_float, "f")), "f");
        } else {
          __classPrivateFieldSet9(this, _PostEffectPass_backbuffer, new Backbuffer(ctx, width, height, pixelRatio, __classPrivateFieldGet10(this, _PostEffectPass_float, "f")), "f");
        }
      }
    }
    resizeBackbuffer(width, height) {
      if (__classPrivateFieldGet10(this, _PostEffectPass_backbuffer, "f") && !__classPrivateFieldGet10(this, _PostEffectPass_size, "f")) {
        __classPrivateFieldGet10(this, _PostEffectPass_backbuffer, "f").resize(width, height);
      }
    }
    /**
     * Register a named buffer texture as a uniform (for auto-binding).
     * The texture value will be updated each frame by the render loop.
     */
    registerBufferUniform(name) {
      if (!__classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f")[name]) {
        __classPrivateFieldGet10(this, _PostEffectPass_uniforms, "f")[name] = { value: null };
      }
    }
    get backbuffer() {
      return __classPrivateFieldGet10(this, _PostEffectPass_backbuffer, "f");
    }
    get persistent() {
      return __classPrivateFieldGet10(this, _PostEffectPass_persistent, "f");
    }
    get float() {
      return __classPrivateFieldGet10(this, _PostEffectPass_float, "f");
    }
    get size() {
      return __classPrivateFieldGet10(this, _PostEffectPass_size, "f");
    }
    dispose() {
      var _a;
      this.pass.dispose();
      (_a = __classPrivateFieldGet10(this, _PostEffectPass_backbuffer, "f")) == null ? void 0 : _a.dispose();
    }
  };
  _PostEffectPass_uniforms = /* @__PURE__ */ new WeakMap(), _PostEffectPass_uniformGenerators = /* @__PURE__ */ new WeakMap(), _PostEffectPass_backbuffer = /* @__PURE__ */ new WeakMap(), _PostEffectPass_persistent = /* @__PURE__ */ new WeakMap(), _PostEffectPass_float = /* @__PURE__ */ new WeakMap(), _PostEffectPass_size = /* @__PURE__ */ new WeakMap();

  // node_modules/@vfx-js/core/lib/esm/program-cache.js
  var __classPrivateFieldSet10 = function(receiver, state2, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state2.set(receiver, value), value;
  };
  var __classPrivateFieldGet11 = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _ProgramCache_glCtx;
  var _ProgramCache_programs;
  var ProgramCache = class {
    constructor(glCtx) {
      _ProgramCache_glCtx.set(this, void 0);
      _ProgramCache_programs.set(this, /* @__PURE__ */ new Map());
      __classPrivateFieldSet10(this, _ProgramCache_glCtx, glCtx, "f");
    }
    get(vert, frag, glslVersion) {
      const key = `${frag}\0${vert}\0${glslVersion != null ? glslVersion : ""}`;
      let p = __classPrivateFieldGet11(this, _ProgramCache_programs, "f").get(key);
      if (!p) {
        p = new Program(__classPrivateFieldGet11(this, _ProgramCache_glCtx, "f"), vert, frag, glslVersion);
        __classPrivateFieldGet11(this, _ProgramCache_programs, "f").set(key, p);
      }
      return p;
    }
    /** Test-only count of cached programs. @internal */
    get size() {
      return __classPrivateFieldGet11(this, _ProgramCache_programs, "f").size;
    }
    dispose() {
      for (const p of __classPrivateFieldGet11(this, _ProgramCache_programs, "f").values()) {
        p.dispose();
      }
      __classPrivateFieldGet11(this, _ProgramCache_programs, "f").clear();
    }
  };
  _ProgramCache_glCtx = /* @__PURE__ */ new WeakMap(), _ProgramCache_programs = /* @__PURE__ */ new WeakMap();

  // node_modules/@vfx-js/core/lib/esm/vfx-player.js
  var __classPrivateFieldSet11 = function(receiver, state2, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state2.set(receiver, value), value;
  };
  var __classPrivateFieldGet12 = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _VFXPlayer_instances;
  var _VFXPlayer_opts;
  var _VFXPlayer_canvas;
  var _VFXPlayer_ctx;
  var _VFXPlayer_gl;
  var _VFXPlayer_quad;
  var _VFXPlayer_programCache;
  var _VFXPlayer_copyPass;
  var _VFXPlayer_postEffectEntries;
  var _VFXPlayer_postEffectTarget;
  var _VFXPlayer_postEffectBufferTargets;
  var _VFXPlayer_postEffectChain;
  var _VFXPlayer_postEffectChainReady;
  var _VFXPlayer_registeredEffects;
  var _VFXPlayer_postEffectChainStaticUniforms;
  var _VFXPlayer_postEffectChainGenerators;
  var _VFXPlayer_postEffectChainLastTime;
  var _VFXPlayer_playRequest;
  var _VFXPlayer_pixelRatio;
  var _VFXPlayer_elements;
  var _VFXPlayer_initTime;
  var _VFXPlayer_canvasRect;
  var _VFXPlayer_viewport;
  var _VFXPlayer_canvasSize;
  var _VFXPlayer_paddingX;
  var _VFXPlayer_paddingY;
  var _VFXPlayer_mouseX;
  var _VFXPlayer_mouseY;
  var _VFXPlayer_isRenderingToCanvas;
  var _VFXPlayer_updateCanvasSize;
  var _VFXPlayer_resize;
  var _VFXPlayer_pointermove;
  var _VFXPlayer_rerenderTextElement;
  var _VFXPlayer_addEffectElement;
  var _VFXPlayer_normalizePasses;
  var _VFXPlayer_playLoop;
  var _VFXPlayer_renderEffectElement;
  var _VFXPlayer_shouldUsePostEffect;
  var _VFXPlayer_assertEffectsNotReused;
  var _VFXPlayer_releaseEffects;
  var _VFXPlayer_chainMarginCss;
  var _VFXPlayer_hitTest;
  var _VFXPlayer_getShader;
  var _VFXPlayer_render;
  var _VFXPlayer_setOffset;
  var _VFXPlayer_initPostEffects;
  var _VFXPlayer_initPostEffectChain;
  var _VFXPlayer_runPostEffectChain;
  var _VFXPlayer_renderPostEffects;
  var _VFXPlayer_setupPostEffectTarget;
  var gifFor = /* @__PURE__ */ new Map();
  var VFXPlayer = class {
    constructor(opts, canvas) {
      _VFXPlayer_instances.add(this);
      _VFXPlayer_opts.set(this, void 0);
      _VFXPlayer_canvas.set(this, void 0);
      _VFXPlayer_ctx.set(this, void 0);
      _VFXPlayer_gl.set(this, void 0);
      _VFXPlayer_quad.set(this, void 0);
      _VFXPlayer_programCache.set(this, void 0);
      _VFXPlayer_copyPass.set(this, void 0);
      _VFXPlayer_postEffectEntries.set(this, []);
      _VFXPlayer_postEffectTarget.set(this, void 0);
      _VFXPlayer_postEffectBufferTargets.set(this, /* @__PURE__ */ new Map());
      _VFXPlayer_postEffectChain.set(this, null);
      _VFXPlayer_postEffectChainReady.set(this, false);
      _VFXPlayer_registeredEffects.set(this, /* @__PURE__ */ new WeakSet());
      _VFXPlayer_postEffectChainStaticUniforms.set(this, {});
      _VFXPlayer_postEffectChainGenerators.set(this, {});
      _VFXPlayer_postEffectChainLastTime.set(this, 0);
      _VFXPlayer_playRequest.set(this, void 0);
      _VFXPlayer_pixelRatio.set(this, 2);
      _VFXPlayer_elements.set(this, []);
      _VFXPlayer_initTime.set(this, Date.now() / 1e3);
      _VFXPlayer_canvasRect.set(this, createRect(0));
      _VFXPlayer_viewport.set(this, createRect(0));
      _VFXPlayer_canvasSize.set(this, [0, 0]);
      _VFXPlayer_paddingX.set(this, 0);
      _VFXPlayer_paddingY.set(this, 0);
      _VFXPlayer_mouseX.set(this, 0);
      _VFXPlayer_mouseY.set(this, 0);
      _VFXPlayer_isRenderingToCanvas.set(this, /* @__PURE__ */ new WeakMap());
      _VFXPlayer_resize.set(this, async () => {
        if (typeof window !== "undefined") {
          for (const e of __classPrivateFieldGet12(this, _VFXPlayer_elements, "f")) {
            if (e.type === "text" && e.isInViewport) {
              const rect = e.element.getBoundingClientRect();
              const w = Math.ceil(rect.width);
              const h = Math.ceil(rect.height);
              if (w !== e.width || h !== e.height) {
                await __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_rerenderTextElement).call(this, e);
                e.width = w;
                e.height = h;
              }
            }
          }
          for (const e of __classPrivateFieldGet12(this, _VFXPlayer_elements, "f")) {
            if (e.type === "text" && !e.isInViewport) {
              const rect = e.element.getBoundingClientRect();
              const w = Math.ceil(rect.width);
              const h = Math.ceil(rect.height);
              if (w !== e.width || h !== e.height) {
                await __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_rerenderTextElement).call(this, e);
                e.width = w;
                e.height = h;
              }
            }
          }
        }
      });
      _VFXPlayer_pointermove.set(this, (e) => {
        if (typeof window !== "undefined") {
          __classPrivateFieldSet11(this, _VFXPlayer_mouseX, e.clientX, "f");
          __classPrivateFieldSet11(this, _VFXPlayer_mouseY, window.innerHeight - e.clientY, "f");
        }
      });
      _VFXPlayer_playLoop.set(this, () => {
        if (this.isPlaying()) {
          this.render();
          __classPrivateFieldSet11(this, _VFXPlayer_playRequest, requestAnimationFrame(__classPrivateFieldGet12(this, _VFXPlayer_playLoop, "f")), "f");
        }
      });
      __classPrivateFieldSet11(this, _VFXPlayer_opts, opts, "f");
      __classPrivateFieldSet11(this, _VFXPlayer_canvas, canvas, "f");
      __classPrivateFieldSet11(this, _VFXPlayer_ctx, new GLContext(canvas), "f");
      __classPrivateFieldSet11(this, _VFXPlayer_gl, __classPrivateFieldGet12(this, _VFXPlayer_ctx, "f").gl, "f");
      __classPrivateFieldGet12(this, _VFXPlayer_gl, "f").clearColor(0, 0, 0, 0);
      __classPrivateFieldSet11(this, _VFXPlayer_pixelRatio, opts.pixelRatio, "f");
      __classPrivateFieldSet11(this, _VFXPlayer_quad, new Quad(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f")), "f");
      __classPrivateFieldSet11(this, _VFXPlayer_programCache, new ProgramCache(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f")), "f");
      if (typeof window !== "undefined") {
        window.addEventListener("resize", __classPrivateFieldGet12(this, _VFXPlayer_resize, "f"));
        window.addEventListener("pointermove", __classPrivateFieldGet12(this, _VFXPlayer_pointermove, "f"));
      }
      __classPrivateFieldGet12(this, _VFXPlayer_resize, "f").call(this);
      __classPrivateFieldSet11(this, _VFXPlayer_copyPass, new CopyPass(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f")), "f");
      __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_initPostEffects).call(this, opts.postEffects);
      __classPrivateFieldGet12(this, _VFXPlayer_ctx, "f").onContextRestored(() => {
        __classPrivateFieldGet12(this, _VFXPlayer_gl, "f").clearColor(0, 0, 0, 0);
      });
    }
    destroy() {
      var _a;
      this.stop();
      if (typeof window !== "undefined") {
        window.removeEventListener("resize", __classPrivateFieldGet12(this, _VFXPlayer_resize, "f"));
        window.removeEventListener("pointermove", __classPrivateFieldGet12(this, _VFXPlayer_pointermove, "f"));
      }
      (_a = __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f")) == null ? void 0 : _a.dispose();
      for (const rt of __classPrivateFieldGet12(this, _VFXPlayer_postEffectBufferTargets, "f").values()) {
        rt == null ? void 0 : rt.dispose();
      }
      for (const e of __classPrivateFieldGet12(this, _VFXPlayer_postEffectEntries, "f")) {
        e.pass.dispose();
      }
      if (__classPrivateFieldGet12(this, _VFXPlayer_postEffectChain, "f")) {
        __classPrivateFieldGet12(this, _VFXPlayer_postEffectChain, "f").dispose();
        __classPrivateFieldSet11(this, _VFXPlayer_postEffectChain, null, "f");
        __classPrivateFieldSet11(this, _VFXPlayer_postEffectChainReady, false, "f");
      }
      __classPrivateFieldGet12(this, _VFXPlayer_copyPass, "f").dispose();
      __classPrivateFieldGet12(this, _VFXPlayer_programCache, "f").dispose();
      __classPrivateFieldGet12(this, _VFXPlayer_quad, "f").dispose();
    }
    async addElement(element, opts = {}, initialCapture) {
      var _a, _b, _c, _d;
      if (opts.effect !== void 0) {
        return __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_addEffectElement).call(this, element, opts, opts.effect, initialCapture);
      }
      const inputPasses = __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_normalizePasses).call(this, opts);
      const domRect = element.getBoundingClientRect();
      const rect = isTextPathElement(element) ? toCeiledRect(domRect) : toRect(domRect);
      const [isFullScreen, overflow] = parseOverflowOpts(opts.overflow);
      const rectWithOverflow = growRect(rect, overflow);
      const intersectionOpts = parseIntersectionOpts(opts.intersection);
      const originalOpacity = element.style.opacity === "" ? 1 : Number.parseFloat(element.style.opacity);
      let texture;
      let type;
      let isGif = false;
      if (element instanceof HTMLImageElement) {
        type = "img";
        isGif = !!element.src.match(/\.gif/i);
        if (isGif) {
          const gif = await GIFData.create(element.src, __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
          gifFor.set(element, gif);
          texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), gif.getCanvas());
        } else {
          const img = await loadImage(element.src);
          texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), img);
        }
      } else if (element instanceof HTMLVideoElement) {
        texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), element);
        type = "video";
      } else if (element instanceof HTMLCanvasElement) {
        if (element.hasAttribute("layoutsubtree") && initialCapture) {
          texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), initialCapture);
          type = "hic";
        } else {
          texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), element);
          type = "canvas";
        }
      } else {
        const canvas = await getCanvasFromElement(element, originalOpacity, void 0, this.maxTextureSize);
        texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), canvas);
        type = "text";
      }
      const [wrapS, wrapT] = parseWrap(opts.wrap);
      texture.wrapS = wrapS;
      texture.wrapT = wrapT;
      texture.needsUpdate = true;
      const autoCrop = (_a = opts.autoCrop) != null ? _a : true;
      if (type === "hic") {
      } else if (opts.overlay === true) {
      } else if (typeof opts.overlay === "number") {
        element.style.setProperty("opacity", opts.overlay.toString());
      } else {
        const opacity = type === "video" ? "0.0001" : "0";
        element.style.setProperty("opacity", opacity.toString());
      }
      const sharedUniforms = {
        src: { value: texture },
        resolution: { value: new Vec2() },
        offset: { value: new Vec2() },
        time: { value: 0 },
        enterTime: { value: -1 },
        leaveTime: { value: -1 },
        mouse: { value: new Vec2() },
        intersection: { value: 0 },
        viewport: { value: new Vec4() },
        autoCrop: { value: autoCrop }
      };
      const sharedUniformGenerators = {};
      if (opts.uniforms !== void 0) {
        for (const [key, value] of Object.entries(opts.uniforms)) {
          if (typeof value === "function") {
            sharedUniforms[key] = { value: value() };
            sharedUniformGenerators[key] = value;
          } else {
            sharedUniforms[key] = { value };
          }
        }
      }
      let backbuffer;
      if (opts.backbuffer) {
        backbuffer = (() => {
          const bw = (rectWithOverflow.right - rectWithOverflow.left) * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
          const bh = (rectWithOverflow.bottom - rectWithOverflow.top) * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
          return new Backbuffer(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), bw, bh, __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), false);
        })();
        sharedUniforms["backbuffer"] = { value: backbuffer.texture };
      }
      const bufferTargets = /* @__PURE__ */ new Map();
      const passBackbuffers = /* @__PURE__ */ new Map();
      for (let i = 0; i < inputPasses.length - 1; i++) {
        const targetName = (_b = inputPasses[i].target) != null ? _b : `pass${i}`;
        inputPasses[i] = __spreadProps(__spreadValues({}, inputPasses[i]), { target: targetName });
        const passSize = inputPasses[i].size;
        const bw = passSize ? passSize[0] : (rectWithOverflow.right - rectWithOverflow.left) * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
        const bh = passSize ? passSize[1] : (rectWithOverflow.bottom - rectWithOverflow.top) * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
        if (inputPasses[i].persistent) {
          const pixelRatio = passSize ? 1 : __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
          const cssW = passSize ? passSize[0] : rectWithOverflow.right - rectWithOverflow.left;
          const cssH = passSize ? passSize[1] : rectWithOverflow.bottom - rectWithOverflow.top;
          passBackbuffers.set(targetName, new Backbuffer(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), cssW, cssH, pixelRatio, inputPasses[i].float));
        } else {
          bufferTargets.set(targetName, createRenderTarget(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), bw, bh, {
            float: inputPasses[i].float
          }));
        }
      }
      const passes = [];
      for (let i = 0; i < inputPasses.length; i++) {
        const p = inputPasses[i];
        const frag = p.frag;
        const passUniforms = __spreadValues({}, sharedUniforms);
        const passUniformGenerators = {};
        for (const [name, rt] of bufferTargets) {
          if (name === p.target) {
            continue;
          }
          if (frag.match(new RegExp(`uniform\\s+sampler2D\\s+${name}\\b`))) {
            passUniforms[name] = { value: rt.texture };
          }
        }
        for (const [name, bb] of passBackbuffers) {
          if (frag.match(new RegExp(`uniform\\s+sampler2D\\s+${name}\\b`))) {
            passUniforms[name] = { value: bb.texture };
          }
        }
        if (p.uniforms) {
          for (const [key, value] of Object.entries(p.uniforms)) {
            if (typeof value === "function") {
              passUniforms[key] = { value: value() };
              passUniformGenerators[key] = value;
            } else {
              passUniforms[key] = { value };
            }
          }
        }
        const pass = createPassMaterial(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), {
          vertexShader: p.vert,
          fragmentShader: frag,
          uniforms: passUniforms,
          renderingToBuffer: p.target !== void 0,
          glslVersion: p.glslVersion
        });
        passes.push({
          pass,
          uniforms: passUniforms,
          uniformGenerators: __spreadValues(__spreadValues({}, sharedUniformGenerators), passUniformGenerators),
          target: p.target,
          persistent: p.persistent,
          float: p.float,
          size: p.size,
          backbuffer: p.target ? passBackbuffers.get(p.target) : void 0
        });
      }
      const now = Date.now() / 1e3;
      const elem = {
        type,
        element,
        isInViewport: false,
        isInLogicalViewport: false,
        // Match the (possibly-ceiled) rect so #resize's width/height
        // comparison stays in the same coordinate system.
        width: rect.right - rect.left,
        height: rect.bottom - rect.top,
        passes,
        bufferTargets,
        startTime: now,
        enterTime: now,
        leaveTime: Number.NEGATIVE_INFINITY,
        release: (_c = opts.release) != null ? _c : Number.POSITIVE_INFINITY,
        isGif,
        isFullScreen,
        overflow,
        intersection: intersectionOpts,
        originalOpacity,
        srcTexture: texture,
        zIndex: (_d = opts.zIndex) != null ? _d : 0,
        backbuffer,
        autoCrop
      };
      __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_hitTest).call(this, elem, rect, now);
      __classPrivateFieldGet12(this, _VFXPlayer_elements, "f").push(elem);
      __classPrivateFieldGet12(this, _VFXPlayer_elements, "f").sort((a, b) => a.zIndex - b.zIndex);
    }
    /**
     * Replace the effect chain on an already-registered effect-path
     * element. Effects whose reference is unchanged keep their host /
     * init state; only added/removed effects run init/dispose. Throws
     * when the element is not registered, lives on the shader path, or
     * when a *new* effect (not already in the current chain) is already
     * attached to another element/postEffect on this player.
     */
    async updateElementEffects(element, rawEffect) {
      const e = __classPrivateFieldGet12(this, _VFXPlayer_elements, "f").find((x) => x.element === element);
      if (!e) {
        throw new Error("[VFX-JS] updateElementEffects: element not registered");
      }
      if (!e.chain) {
        throw new Error("[VFX-JS] updateElementEffects: element is on the shader path; effect-only updates are not supported");
      }
      const newEffects = Array.isArray(rawEffect) ? [...rawEffect] : [rawEffect];
      const oldEffects = e.chain.effects;
      const oldSet = new Set(oldEffects);
      const reallyNew = [];
      for (const eff of newEffects) {
        if (!oldSet.has(eff)) {
          if (__classPrivateFieldGet12(this, _VFXPlayer_registeredEffects, "f").has(eff)) {
            throw new Error("[VFX-JS] Effect instance already attached. Construct a new instance per `vfx.add()` / `postEffect`.");
          }
          reallyNew.push(eff);
        }
      }
      await e.chain.replaceEffects(newEffects);
      const newSet = new Set(newEffects);
      for (const eff of oldEffects) {
        if (!newSet.has(eff)) {
          __classPrivateFieldGet12(this, _VFXPlayer_registeredEffects, "f").delete(eff);
        }
      }
      for (const eff of reallyNew) {
        __classPrivateFieldGet12(this, _VFXPlayer_registeredEffects, "f").add(eff);
      }
    }
    removeElement(element) {
      var _a, _b;
      const i = __classPrivateFieldGet12(this, _VFXPlayer_elements, "f").findIndex((e) => e.element === element);
      if (i !== -1) {
        const e = __classPrivateFieldGet12(this, _VFXPlayer_elements, "f").splice(i, 1)[0];
        if (e.chain) {
          __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_releaseEffects).call(this, e.chain.effects);
          e.chain.dispose();
        } else {
          for (const rt of e.bufferTargets.values()) {
            rt.dispose();
          }
          for (const p of e.passes) {
            p.pass.dispose();
            (_a = p.backbuffer) == null ? void 0 : _a.dispose();
          }
          (_b = e.backbuffer) == null ? void 0 : _b.dispose();
        }
        e.srcTexture.dispose();
        element.style.setProperty("opacity", e.originalOpacity.toString());
      }
    }
    updateTextElement(element) {
      const i = __classPrivateFieldGet12(this, _VFXPlayer_elements, "f").findIndex((e) => e.element === element);
      if (i !== -1) {
        return __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_rerenderTextElement).call(this, __classPrivateFieldGet12(this, _VFXPlayer_elements, "f")[i]);
      }
      return Promise.resolve();
    }
    /**
     * Re-capture an `<img>` whose `src` changed since `add()`.
     *
     * Image source textures are uploaded once at `add()` time (only
     * video / GIF refresh per frame), so this reloads the current `src`
     * and swaps `e.srcTexture`. No-op for GIFs, which refresh already.
     */
    async updateImageElement(element) {
      const e = __classPrivateFieldGet12(this, _VFXPlayer_elements, "f").find((e2) => e2.element === element);
      if (!e || e.type !== "img" || e.isGif) {
        return;
      }
      const img = await loadImage(element.src);
      const oldTexture = e.srcTexture;
      const texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), img);
      texture.wrapS = oldTexture.wrapS;
      texture.wrapT = oldTexture.wrapT;
      texture.needsUpdate = true;
      if (!e.chain && e.passes.length > 0) {
        e.passes[0].uniforms["src"].value = texture;
      }
      e.srcTexture = texture;
      oldTexture.dispose();
    }
    updateCanvasElement(element) {
      const e = __classPrivateFieldGet12(this, _VFXPlayer_elements, "f").find((e2) => e2.element === element);
      if (e) {
        const oldTexture = e.srcTexture;
        const texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), element);
        texture.wrapS = oldTexture.wrapS;
        texture.wrapT = oldTexture.wrapT;
        texture.needsUpdate = true;
        if (!e.chain && e.passes.length > 0) {
          e.passes[0].uniforms["src"].value = texture;
        }
        e.srcTexture = texture;
        oldTexture.dispose();
      }
    }
    updateHICTexture(canvas, offscreen) {
      const e = __classPrivateFieldGet12(this, _VFXPlayer_elements, "f").find((e2) => e2.element === canvas);
      if (!e || e.type !== "hic") {
        return;
      }
      const oldTexture = e.srcTexture;
      if (oldTexture.source === offscreen) {
        oldTexture.needsUpdate = true;
      } else {
        const texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), offscreen);
        texture.wrapS = oldTexture.wrapS;
        texture.wrapT = oldTexture.wrapT;
        texture.needsUpdate = true;
        if (!e.chain && e.passes.length > 0) {
          e.passes[0].uniforms["src"].value = texture;
        }
        e.srcTexture = texture;
        oldTexture.dispose();
      }
    }
    get maxTextureSize() {
      return __classPrivateFieldGet12(this, _VFXPlayer_ctx, "f").maxTextureSize;
    }
    isPlaying() {
      return __classPrivateFieldGet12(this, _VFXPlayer_playRequest, "f") !== void 0;
    }
    play() {
      if (!this.isPlaying()) {
        __classPrivateFieldSet11(this, _VFXPlayer_playRequest, requestAnimationFrame(__classPrivateFieldGet12(this, _VFXPlayer_playLoop, "f")), "f");
      }
    }
    stop() {
      if (__classPrivateFieldGet12(this, _VFXPlayer_playRequest, "f") !== void 0) {
        cancelAnimationFrame(__classPrivateFieldGet12(this, _VFXPlayer_playRequest, "f"));
        __classPrivateFieldSet11(this, _VFXPlayer_playRequest, void 0, "f");
      }
    }
    render() {
      var _a;
      const now = Date.now() / 1e3;
      const gl = __classPrivateFieldGet12(this, _VFXPlayer_gl, "f");
      __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_updateCanvasSize).call(this);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      gl.viewport(0, 0, __classPrivateFieldGet12(this, _VFXPlayer_canvas, "f").width, __classPrivateFieldGet12(this, _VFXPlayer_canvas, "f").height);
      gl.clear(gl.COLOR_BUFFER_BIT);
      const canvasW = __classPrivateFieldGet12(this, _VFXPlayer_canvasRect, "f").right - __classPrivateFieldGet12(this, _VFXPlayer_canvasRect, "f").left;
      const canvasH = __classPrivateFieldGet12(this, _VFXPlayer_canvasRect, "f").bottom - __classPrivateFieldGet12(this, _VFXPlayer_canvasRect, "f").top;
      const viewportGlRect = getGLRect(0, 0, canvasW, canvasH);
      const shouldUsePostEffect = __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_shouldUsePostEffect).call(this);
      if (shouldUsePostEffect) {
        __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_setupPostEffectTarget).call(this, canvasW, canvasH);
        if (__classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f")) {
          gl.bindFramebuffer(gl.FRAMEBUFFER, __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f").fbo);
          gl.clear(gl.COLOR_BUFFER_BIT);
          gl.bindFramebuffer(gl.FRAMEBUFFER, null);
        }
      }
      for (const e of __classPrivateFieldGet12(this, _VFXPlayer_elements, "f")) {
        const domRect = e.element.getBoundingClientRect();
        const rect = e.type === "text" ? toCeiledRect(domRect) : toRect(domRect);
        const hit = __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_hitTest).call(this, e, rect, now);
        if (!hit.isVisible) {
          continue;
        }
        if (e.chain) {
          __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_renderEffectElement).call(this, e, rect, hit, now);
          continue;
        }
        const u = e.passes[0].uniforms;
        u["time"].value = now - e.startTime;
        u["resolution"].value.set((rect.right - rect.left) * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), (rect.bottom - rect.top) * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
        u["mouse"].value.set((__classPrivateFieldGet12(this, _VFXPlayer_mouseX, "f") + __classPrivateFieldGet12(this, _VFXPlayer_paddingX, "f")) * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), (__classPrivateFieldGet12(this, _VFXPlayer_mouseY, "f") + __classPrivateFieldGet12(this, _VFXPlayer_paddingY, "f")) * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
        for (const pass of e.passes) {
          for (const [key, gen] of Object.entries(pass.uniformGenerators)) {
            pass.uniforms[key].value = gen();
          }
        }
        (_a = gifFor.get(e.element)) == null ? void 0 : _a.update();
        if (e.type === "video" || e.isGif) {
          u["src"].value.needsUpdate = true;
        }
        const glRect = rectToGLRect(rect, canvasH, __classPrivateFieldGet12(this, _VFXPlayer_paddingX, "f"), __classPrivateFieldGet12(this, _VFXPlayer_paddingY, "f"));
        const glRectWithOverflow = rectToGLRect(hit.rectWithOverflow, canvasH, __classPrivateFieldGet12(this, _VFXPlayer_paddingX, "f"), __classPrivateFieldGet12(this, _VFXPlayer_paddingY, "f"));
        if (e.backbuffer) {
          e.passes[0].uniforms["backbuffer"].value = e.backbuffer.texture;
        }
        {
          const targetRect = e.isFullScreen ? viewportGlRect : glRectWithOverflow;
          const tw = Math.max(1, targetRect.w * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
          const th = Math.max(1, targetRect.h * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
          const cssW = Math.max(1, targetRect.w);
          const cssH = Math.max(1, targetRect.h);
          for (let i = 0; i < e.passes.length - 1; i++) {
            const pass = e.passes[i];
            if (pass.size) {
              continue;
            }
            if (pass.backbuffer) {
              pass.backbuffer.resize(cssW, cssH);
            } else {
              const rt = e.bufferTargets.get(pass.target);
              if (rt && (rt.width !== tw || rt.height !== th)) {
                rt.setSize(tw, th);
              }
            }
          }
        }
        const resolvedTargets = /* @__PURE__ */ new Map();
        for (const pass of e.passes) {
          if (pass.backbuffer && pass.target) {
            resolvedTargets.set(pass.target, pass.backbuffer.texture);
          }
        }
        let inputTexture = e.srcTexture;
        const relMouseX = __classPrivateFieldGet12(this, _VFXPlayer_mouseX, "f") + __classPrivateFieldGet12(this, _VFXPlayer_paddingX, "f") - glRect.x;
        const relMouseY = __classPrivateFieldGet12(this, _VFXPlayer_mouseY, "f") + __classPrivateFieldGet12(this, _VFXPlayer_paddingY, "f") - glRect.y;
        for (let i = 0; i < e.passes.length - 1; i++) {
          const pass = e.passes[i];
          const defaultRect = e.isFullScreen ? viewportGlRect : glRectWithOverflow;
          pass.uniforms["src"].value = inputTexture;
          for (const [name, tex] of resolvedTargets) {
            if (pass.uniforms[name]) {
              pass.uniforms[name].value = tex;
            }
          }
          for (const [key, gen] of Object.entries(pass.uniformGenerators)) {
            if (pass.uniforms[key]) {
              pass.uniforms[key].value = gen();
            }
          }
          const bufferW = pass.size ? pass.size[0] : defaultRect.w * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
          const bufferH = pass.size ? pass.size[1] : defaultRect.h * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
          const bufferRect = pass.size ? getGLRect(0, 0, pass.size[0], pass.size[1]) : getGLRect(0, 0, defaultRect.w, defaultRect.h);
          pass.uniforms["resolution"].value.set(bufferW, bufferH);
          pass.uniforms["offset"].value.set(0, 0);
          pass.uniforms["mouse"].value.set(relMouseX / defaultRect.w * bufferW, relMouseY / defaultRect.h * bufferH);
          if (pass.backbuffer) {
            __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_render).call(this, pass.pass, pass.backbuffer.target, bufferRect, pass.uniforms, true);
            pass.backbuffer.swap();
            inputTexture = pass.backbuffer.texture;
          } else {
            const rt = e.bufferTargets.get(pass.target);
            if (!rt) {
              continue;
            }
            __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_render).call(this, pass.pass, rt, bufferRect, pass.uniforms, true);
            inputTexture = rt.texture;
          }
          if (pass.target) {
            resolvedTargets.set(pass.target, inputTexture);
          }
        }
        const finalPass = e.passes[e.passes.length - 1];
        finalPass.uniforms["src"].value = inputTexture;
        finalPass.uniforms["resolution"].value.set(domRect.width * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), domRect.height * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
        finalPass.uniforms["offset"].value.set(glRect.x * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), glRect.y * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
        finalPass.uniforms["mouse"].value.set((__classPrivateFieldGet12(this, _VFXPlayer_mouseX, "f") + __classPrivateFieldGet12(this, _VFXPlayer_paddingX, "f")) * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), (__classPrivateFieldGet12(this, _VFXPlayer_mouseY, "f") + __classPrivateFieldGet12(this, _VFXPlayer_paddingY, "f")) * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
        for (const [name, tex] of resolvedTargets) {
          if (finalPass.uniforms[name]) {
            finalPass.uniforms[name].value = tex;
          }
        }
        for (const [key, gen] of Object.entries(finalPass.uniformGenerators)) {
          if (finalPass.uniforms[key]) {
            finalPass.uniforms[key].value = gen();
          }
        }
        if (e.backbuffer) {
          finalPass.uniforms["backbuffer"].value = e.backbuffer.texture;
          if (e.isFullScreen) {
            e.backbuffer.resize(canvasW, canvasH);
            __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_setOffset).call(this, e, glRect.x, glRect.y);
            __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_render).call(this, finalPass.pass, e.backbuffer.target, viewportGlRect, finalPass.uniforms, true);
            e.backbuffer.swap();
            __classPrivateFieldGet12(this, _VFXPlayer_copyPass, "f").setUniforms(e.backbuffer.texture, __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), viewportGlRect);
            __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_render).call(this, __classPrivateFieldGet12(this, _VFXPlayer_copyPass, "f").pass, shouldUsePostEffect ? __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f") || null : null, viewportGlRect, __classPrivateFieldGet12(this, _VFXPlayer_copyPass, "f").uniforms, false);
          } else {
            e.backbuffer.resize(glRectWithOverflow.w, glRectWithOverflow.h);
            __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_setOffset).call(this, e, e.overflow.left, e.overflow.bottom);
            __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_render).call(this, finalPass.pass, e.backbuffer.target, e.backbuffer.getViewport(), finalPass.uniforms, true);
            e.backbuffer.swap();
            __classPrivateFieldGet12(this, _VFXPlayer_copyPass, "f").setUniforms(e.backbuffer.texture, __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), glRectWithOverflow);
            __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_render).call(this, __classPrivateFieldGet12(this, _VFXPlayer_copyPass, "f").pass, shouldUsePostEffect ? __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f") || null : null, glRectWithOverflow, __classPrivateFieldGet12(this, _VFXPlayer_copyPass, "f").uniforms, false);
          }
        } else {
          __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_setOffset).call(this, e, glRect.x, glRect.y);
          __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_render).call(this, finalPass.pass, shouldUsePostEffect ? __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f") || null : null, e.isFullScreen ? viewportGlRect : glRectWithOverflow, finalPass.uniforms, false);
        }
      }
      if (shouldUsePostEffect && __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f")) {
        if (__classPrivateFieldGet12(this, _VFXPlayer_postEffectChain, "f") && __classPrivateFieldGet12(this, _VFXPlayer_postEffectChainReady, "f")) {
          __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_runPostEffectChain).call(this, viewportGlRect, now);
        } else {
          __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_renderPostEffects).call(this, viewportGlRect, now);
        }
      }
    }
  };
  _VFXPlayer_opts = /* @__PURE__ */ new WeakMap(), _VFXPlayer_canvas = /* @__PURE__ */ new WeakMap(), _VFXPlayer_ctx = /* @__PURE__ */ new WeakMap(), _VFXPlayer_gl = /* @__PURE__ */ new WeakMap(), _VFXPlayer_quad = /* @__PURE__ */ new WeakMap(), _VFXPlayer_programCache = /* @__PURE__ */ new WeakMap(), _VFXPlayer_copyPass = /* @__PURE__ */ new WeakMap(), _VFXPlayer_postEffectEntries = /* @__PURE__ */ new WeakMap(), _VFXPlayer_postEffectTarget = /* @__PURE__ */ new WeakMap(), _VFXPlayer_postEffectBufferTargets = /* @__PURE__ */ new WeakMap(), _VFXPlayer_postEffectChain = /* @__PURE__ */ new WeakMap(), _VFXPlayer_postEffectChainReady = /* @__PURE__ */ new WeakMap(), _VFXPlayer_registeredEffects = /* @__PURE__ */ new WeakMap(), _VFXPlayer_postEffectChainStaticUniforms = /* @__PURE__ */ new WeakMap(), _VFXPlayer_postEffectChainGenerators = /* @__PURE__ */ new WeakMap(), _VFXPlayer_postEffectChainLastTime = /* @__PURE__ */ new WeakMap(), _VFXPlayer_playRequest = /* @__PURE__ */ new WeakMap(), _VFXPlayer_pixelRatio = /* @__PURE__ */ new WeakMap(), _VFXPlayer_elements = /* @__PURE__ */ new WeakMap(), _VFXPlayer_initTime = /* @__PURE__ */ new WeakMap(), _VFXPlayer_canvasRect = /* @__PURE__ */ new WeakMap(), _VFXPlayer_viewport = /* @__PURE__ */ new WeakMap(), _VFXPlayer_canvasSize = /* @__PURE__ */ new WeakMap(), _VFXPlayer_paddingX = /* @__PURE__ */ new WeakMap(), _VFXPlayer_paddingY = /* @__PURE__ */ new WeakMap(), _VFXPlayer_mouseX = /* @__PURE__ */ new WeakMap(), _VFXPlayer_mouseY = /* @__PURE__ */ new WeakMap(), _VFXPlayer_isRenderingToCanvas = /* @__PURE__ */ new WeakMap(), _VFXPlayer_resize = /* @__PURE__ */ new WeakMap(), _VFXPlayer_pointermove = /* @__PURE__ */ new WeakMap(), _VFXPlayer_playLoop = /* @__PURE__ */ new WeakMap(), _VFXPlayer_instances = /* @__PURE__ */ new WeakSet(), _VFXPlayer_updateCanvasSize = function _VFXPlayer_updateCanvasSize2() {
    if (typeof window === "undefined") {
      return;
    }
    const doc = __classPrivateFieldGet12(this, _VFXPlayer_canvas, "f").ownerDocument;
    const viewportEl = doc.compatMode === "BackCompat" ? doc.body : doc.documentElement;
    const width = viewportEl.clientWidth;
    const height = viewportEl.clientHeight;
    const scrollX = window.scrollX;
    const scrollY = window.scrollY;
    let paddingX;
    let paddingY;
    if (__classPrivateFieldGet12(this, _VFXPlayer_opts, "f").fixedCanvas) {
      paddingX = 0;
      paddingY = 0;
    } else if (__classPrivateFieldGet12(this, _VFXPlayer_opts, "f").wrapper) {
      paddingX = width * __classPrivateFieldGet12(this, _VFXPlayer_opts, "f").scrollPadding[0];
      paddingY = height * __classPrivateFieldGet12(this, _VFXPlayer_opts, "f").scrollPadding[1];
    } else {
      const maxPaddingX = doc.body.scrollWidth - (scrollX + width);
      const maxPaddingY = doc.body.scrollHeight - (scrollY + height);
      paddingX = clamp2(width * __classPrivateFieldGet12(this, _VFXPlayer_opts, "f").scrollPadding[0], 0, maxPaddingX);
      paddingY = clamp2(height * __classPrivateFieldGet12(this, _VFXPlayer_opts, "f").scrollPadding[1], 0, maxPaddingY);
    }
    const widthWithPadding = width + paddingX * 2;
    const heightWithPadding = height + paddingY * 2;
    if (widthWithPadding !== __classPrivateFieldGet12(this, _VFXPlayer_canvasSize, "f")[0] || heightWithPadding !== __classPrivateFieldGet12(this, _VFXPlayer_canvasSize, "f")[1]) {
      __classPrivateFieldGet12(this, _VFXPlayer_canvas, "f").style.width = `${widthWithPadding}px`;
      __classPrivateFieldGet12(this, _VFXPlayer_canvas, "f").style.height = `${heightWithPadding}px`;
      __classPrivateFieldGet12(this, _VFXPlayer_ctx, "f").setSize(widthWithPadding, heightWithPadding, __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
      __classPrivateFieldSet11(this, _VFXPlayer_canvasRect, createRect({
        top: -paddingY,
        left: -paddingX,
        right: width + paddingX,
        bottom: height + paddingY
      }), "f");
      __classPrivateFieldSet11(this, _VFXPlayer_viewport, createRect({
        top: 0,
        left: 0,
        right: width,
        bottom: height
      }), "f");
      __classPrivateFieldSet11(this, _VFXPlayer_canvasSize, [widthWithPadding, heightWithPadding], "f");
      __classPrivateFieldSet11(this, _VFXPlayer_paddingX, paddingX, "f");
      __classPrivateFieldSet11(this, _VFXPlayer_paddingY, paddingY, "f");
    }
    if (!__classPrivateFieldGet12(this, _VFXPlayer_opts, "f").fixedCanvas) {
      __classPrivateFieldGet12(this, _VFXPlayer_canvas, "f").style.setProperty("transform", `translate(${scrollX - paddingX}px, ${scrollY - paddingY}px)`);
    }
  }, _VFXPlayer_rerenderTextElement = async function _VFXPlayer_rerenderTextElement2(e) {
    if (__classPrivateFieldGet12(this, _VFXPlayer_isRenderingToCanvas, "f").get(e.element)) {
      return;
    }
    __classPrivateFieldGet12(this, _VFXPlayer_isRenderingToCanvas, "f").set(e.element, true);
    try {
      const oldTexture = e.srcTexture;
      const oldCanvas = oldTexture.source instanceof OffscreenCanvas ? oldTexture.source : void 0;
      const canvas = await getCanvasFromElement(e.element, e.originalOpacity, oldCanvas, this.maxTextureSize);
      if (canvas.width === 0 || canvas.width === 0) {
        throw "omg";
      }
      const texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), canvas);
      texture.wrapS = oldTexture.wrapS;
      texture.wrapT = oldTexture.wrapT;
      texture.needsUpdate = true;
      if (!e.chain && e.passes.length > 0) {
        e.passes[0].uniforms["src"].value = texture;
      }
      e.srcTexture = texture;
      oldTexture.dispose();
    } catch (e2) {
      console.error(e2);
    }
    __classPrivateFieldGet12(this, _VFXPlayer_isRenderingToCanvas, "f").set(e.element, false);
  }, _VFXPlayer_addEffectElement = async function _VFXPlayer_addEffectElement2(element, opts, rawEffect, initialCapture) {
    var _a, _b, _c, _d;
    if (opts.shader !== void 0) {
      console.warn("[VFX-JS] Both `shader` and `effect` specified; `effect` takes precedence.");
    }
    if (opts.overflow !== void 0) {
      console.warn("[VFX-JS] `overflow` is shader-path only and is ignored by the effect path. Use each effect's own `outputRect` (with `dims.canvasRect` for fullscreen) to control its dst rect.");
    }
    const effects = Array.isArray(rawEffect) ? [...rawEffect] : [rawEffect];
    __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_assertEffectsNotReused).call(this, effects);
    const domRect = element.getBoundingClientRect();
    const rect = isTextPathElement(element) ? toCeiledRect(domRect) : toRect(domRect);
    const [isFullScreen, overflow] = parseOverflowOpts(opts.overflow);
    const intersectionOpts = parseIntersectionOpts(opts.intersection);
    const originalOpacity = element.style.opacity === "" ? 1 : Number.parseFloat(element.style.opacity);
    let texture;
    let type;
    let isGif = false;
    if (element instanceof HTMLImageElement) {
      type = "img";
      isGif = !!element.src.match(/\.gif/i);
      if (isGif) {
        const gif = await GIFData.create(element.src, __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
        gifFor.set(element, gif);
        texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), gif.getCanvas());
      } else {
        const img = await loadImage(element.src);
        texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), img);
      }
    } else if (element instanceof HTMLVideoElement) {
      texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), element);
      type = "video";
    } else if (element instanceof HTMLCanvasElement) {
      if (element.hasAttribute("layoutsubtree") && initialCapture) {
        texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), initialCapture);
        type = "hic";
      } else {
        texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), element);
        type = "canvas";
      }
    } else {
      const canvas = await getCanvasFromElement(element, originalOpacity, void 0, this.maxTextureSize);
      texture = new Texture(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), canvas);
      type = "text";
    }
    const [wrapS, wrapT] = parseWrap(opts.wrap);
    texture.wrapS = wrapS;
    texture.wrapT = wrapT;
    texture.needsUpdate = true;
    const autoCrop = (_a = opts.autoCrop) != null ? _a : true;
    if (type === "hic") {
    } else if (opts.overlay === true) {
    } else if (typeof opts.overlay === "number") {
      element.style.setProperty("opacity", opts.overlay.toString());
    } else {
      const opacity = type === "video" ? "0.0001" : "0";
      element.style.setProperty("opacity", opacity.toString());
    }
    const now = Date.now() / 1e3;
    const elem = {
      type,
      element,
      isInViewport: false,
      isInLogicalViewport: false,
      // Match the (possibly-ceiled) rect so #resize's width/height
      // comparison stays in the same coordinate system.
      width: rect.right - rect.left,
      height: rect.bottom - rect.top,
      passes: [],
      bufferTargets: /* @__PURE__ */ new Map(),
      startTime: now,
      enterTime: now,
      leaveTime: Number.NEGATIVE_INFINITY,
      release: (_b = opts.release) != null ? _b : Number.POSITIVE_INFINITY,
      isGif,
      isFullScreen,
      overflow,
      intersection: intersectionOpts,
      originalOpacity,
      srcTexture: texture,
      zIndex: (_c = opts.zIndex) != null ? _c : 0,
      backbuffer: void 0,
      autoCrop,
      effectLastRenderTime: now
    };
    const captureHandle = makeEffectTexture(() => elem.srcTexture, () => readTextureSourceDim(elem.srcTexture, "w"), () => readTextureSourceDim(elem.srcTexture, "h"));
    const staticUniforms = {};
    const gens = {};
    if (opts.uniforms) {
      for (const [k, v] of Object.entries(opts.uniforms)) {
        if (typeof v === "function") {
          gens[k] = v;
          staticUniforms[k] = v();
        } else {
          staticUniforms[k] = v;
        }
      }
    }
    elem.effectUniformGenerators = gens;
    elem.effectStaticUniforms = staticUniforms;
    const vfxProps = {
      autoCrop,
      glslVersion: (_d = opts.glslVersion) != null ? _d : "300 es"
    };
    const chain = new EffectChain(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), __classPrivateFieldGet12(this, _VFXPlayer_quad, "f"), __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), effects, vfxProps, captureHandle, false, __classPrivateFieldGet12(this, _VFXPlayer_programCache, "f"));
    try {
      await chain.initAll();
    } catch (err) {
      __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_releaseEffects).call(this, effects);
      texture.dispose();
      element.style.setProperty("opacity", originalOpacity.toString());
      throw err;
    }
    elem.chain = chain;
    __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_hitTest).call(this, elem, rect, now);
    __classPrivateFieldGet12(this, _VFXPlayer_elements, "f").push(elem);
    __classPrivateFieldGet12(this, _VFXPlayer_elements, "f").sort((a, b) => a.zIndex - b.zIndex);
  }, _VFXPlayer_normalizePasses = function _VFXPlayer_normalizePasses2(opts) {
    const inherit = (p) => p.glslVersion === void 0 && opts.glslVersion !== void 0 ? __spreadProps(__spreadValues({}, p), { glslVersion: opts.glslVersion }) : p;
    if (Array.isArray(opts.shader)) {
      return opts.shader.map(inherit);
    }
    const shaderCode = __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_getShader).call(this, opts.shader || "uvGradient");
    return [inherit({ frag: shaderCode })];
  }, _VFXPlayer_renderEffectElement = function _VFXPlayer_renderEffectElement2(e, rect, hit, now) {
    var _a, _b, _c;
    const chain = e.chain;
    if (!chain) {
      return;
    }
    const pr = __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
    (_a = gifFor.get(e.element)) == null ? void 0 : _a.update();
    if (e.type === "video" || e.isGif) {
      e.srcTexture.needsUpdate = true;
    }
    const resolvedUniforms = __spreadValues({}, (_b = e.effectStaticUniforms) != null ? _b : {});
    if (e.effectUniformGenerators) {
      for (const [k, gen] of Object.entries(e.effectUniformGenerators)) {
        resolvedUniforms[k] = gen();
      }
    }
    const canvasW = __classPrivateFieldGet12(this, _VFXPlayer_canvasRect, "f").right - __classPrivateFieldGet12(this, _VFXPlayer_canvasRect, "f").left;
    const canvasH = __classPrivateFieldGet12(this, _VFXPlayer_canvasRect, "f").bottom - __classPrivateFieldGet12(this, _VFXPlayer_canvasRect, "f").top;
    const glRect = rectToGLRect(rect, canvasH, __classPrivateFieldGet12(this, _VFXPlayer_paddingX, "f"), __classPrivateFieldGet12(this, _VFXPlayer_paddingY, "f"));
    const relMouseX = __classPrivateFieldGet12(this, _VFXPlayer_mouseX, "f") + __classPrivateFieldGet12(this, _VFXPlayer_paddingX, "f") - glRect.x;
    const relMouseY = __classPrivateFieldGet12(this, _VFXPlayer_mouseY, "f") + __classPrivateFieldGet12(this, _VFXPlayer_paddingY, "f") - glRect.y;
    const elementInnerW = rect.right - rect.left;
    const elementInnerH = rect.bottom - rect.top;
    const prevT = (_c = e.effectLastRenderTime) != null ? _c : now;
    const deltaTime = now - prevT;
    e.effectLastRenderTime = now;
    const shouldUsePostEffect = __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_shouldUsePostEffect).call(this);
    const finalTarget = shouldUsePostEffect && __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f") ? makeEffectRenderTargetFromFb(__classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f")) : null;
    chain.run({
      time: now - e.startTime,
      deltaTime,
      mouse: [relMouseX * pr, relMouseY * pr],
      mouseViewport: [__classPrivateFieldGet12(this, _VFXPlayer_mouseX, "f") * pr, __classPrivateFieldGet12(this, _VFXPlayer_mouseY, "f") * pr],
      intersection: hit.intersection,
      enterTime: now - e.enterTime,
      leaveTime: now - e.leaveTime,
      resolvedUniforms,
      canvasSize: [canvasW, canvasH],
      canvasBufferSize: [canvasW * pr, canvasH * pr],
      elementSize: [elementInnerW, elementInnerH],
      elementBufferSize: [elementInnerW * pr, elementInnerH * pr],
      elementRectOnCanvasPx: {
        x: glRect.x * pr,
        y: glRect.y * pr,
        w: glRect.w * pr,
        h: glRect.h * pr
      },
      finalTarget,
      isVisible: hit.isVisible
    });
  }, _VFXPlayer_shouldUsePostEffect = function _VFXPlayer_shouldUsePostEffect2() {
    return __classPrivateFieldGet12(this, _VFXPlayer_postEffectEntries, "f").length > 0 || __classPrivateFieldGet12(this, _VFXPlayer_postEffectChain, "f") !== null && __classPrivateFieldGet12(this, _VFXPlayer_postEffectChainReady, "f");
  }, _VFXPlayer_assertEffectsNotReused = function _VFXPlayer_assertEffectsNotReused2(effects) {
    for (const e of effects) {
      if (__classPrivateFieldGet12(this, _VFXPlayer_registeredEffects, "f").has(e)) {
        throw new Error("[VFX-JS] Effect instance already attached. Construct a new instance per `vfx.add()` / `postEffect`.");
      }
    }
    for (const e of effects) {
      __classPrivateFieldGet12(this, _VFXPlayer_registeredEffects, "f").add(e);
    }
  }, _VFXPlayer_releaseEffects = function _VFXPlayer_releaseEffects2(effects) {
    for (const e of effects) {
      __classPrivateFieldGet12(this, _VFXPlayer_registeredEffects, "f").delete(e);
    }
  }, _VFXPlayer_chainMarginCss = function _VFXPlayer_chainMarginCss2(chain) {
    const padBuffer = chain.hitTestPadBuffer;
    const pr = __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
    return createMargin({
      top: padBuffer.top / pr,
      right: padBuffer.right / pr,
      bottom: padBuffer.bottom / pr,
      left: padBuffer.left / pr
    });
  }, _VFXPlayer_hitTest = function _VFXPlayer_hitTest2(e, rect, now) {
    const visibilityMargin = e.chain ? __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_chainMarginCss).call(this, e.chain) : e.overflow;
    const rectWithOverflow = growRect(rect, visibilityMargin);
    const isInViewport = e.isFullScreen || isRectInViewport(__classPrivateFieldGet12(this, _VFXPlayer_viewport, "f"), rectWithOverflow);
    const viewportWithMargin = growRect(__classPrivateFieldGet12(this, _VFXPlayer_viewport, "f"), e.intersection.rootMargin);
    const intersection = getIntersection(viewportWithMargin, rect);
    const isInLogicalViewport = e.isFullScreen || checkIntersection(viewportWithMargin, rect, intersection, e.intersection.threshold);
    if (!e.isInLogicalViewport && isInLogicalViewport) {
      e.enterTime = now;
      e.leaveTime = Number.POSITIVE_INFINITY;
    }
    if (e.isInLogicalViewport && !isInLogicalViewport) {
      e.leaveTime = now;
    }
    e.isInViewport = isInViewport;
    e.isInLogicalViewport = isInLogicalViewport;
    const isVisible = isInViewport && now - e.leaveTime <= e.release;
    if (isVisible && !e.chain && e.passes.length > 0) {
      const u = e.passes[0].uniforms;
      u["intersection"].value = intersection;
      u["enterTime"].value = now - e.enterTime;
      u["leaveTime"].value = now - e.leaveTime;
    }
    return { isVisible, intersection, rectWithOverflow };
  }, _VFXPlayer_getShader = function _VFXPlayer_getShader2(shaderNameOrCode) {
    if (shaderNameOrCode in shaders) {
      return shaders[shaderNameOrCode];
    } else {
      return shaderNameOrCode;
    }
  }, _VFXPlayer_render = function _VFXPlayer_render2(pass, target, rect, uniforms, clearTarget) {
    const gl = __classPrivateFieldGet12(this, _VFXPlayer_gl, "f");
    if (clearTarget && target !== null && target !== __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f")) {
      gl.bindFramebuffer(gl.FRAMEBUFFER, target.fbo);
      gl.viewport(0, 0, target.width, target.height);
      gl.clear(gl.COLOR_BUFFER_BIT);
    }
    const vp = uniforms["viewport"];
    if (vp && vp.value instanceof Vec4) {
      vp.value.set(rect.x * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), rect.y * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), rect.w * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), rect.h * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
    }
    try {
      renderPass(gl, __classPrivateFieldGet12(this, _VFXPlayer_quad, "f"), pass, target, rect, __classPrivateFieldGet12(this, _VFXPlayer_canvasSize, "f")[0], __classPrivateFieldGet12(this, _VFXPlayer_canvasSize, "f")[1], __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
    } catch (e) {
      console.error(e);
    }
  }, _VFXPlayer_setOffset = function _VFXPlayer_setOffset2(e, x, y) {
    const offset = e.passes[0].uniforms["offset"].value;
    offset.x = x * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
    offset.y = y * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
  }, _VFXPlayer_initPostEffects = function _VFXPlayer_initPostEffects2(postEffects) {
    var _a, _b, _c, _d;
    const pe = postEffects.length === 1 && !("frag" in postEffects[0]) ? postEffects[0] : null;
    if (pe && pe.effect !== void 0) {
      __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_initPostEffectChain).call(this, pe, pe.effect);
      return;
    }
    const shaderSources = [];
    const passItems = [];
    for (const pe2 of postEffects) {
      if ("frag" in pe2) {
        passItems.push(pe2);
      }
    }
    for (let i = 0; i < passItems.length - 1; i++) {
      if (!passItems[i].target) {
        passItems[i] = __spreadProps(__spreadValues({}, passItems[i]), { target: `pass${i}` });
      }
    }
    for (const pe2 of postEffects) {
      let frag;
      let pass;
      let target;
      if ("frag" in pe2) {
        frag = pe2.frag;
        pass = new PostEffectPass(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), frag, pe2.uniforms, (_a = pe2.persistent) != null ? _a : false, (_b = pe2.float) != null ? _b : false, pe2.size, pe2.target !== void 0, pe2.glslVersion);
        target = pe2.target;
      } else {
        if (pe2.shader === void 0) {
          throw new Error("VFXPostEffect requires `shader` (the `effect` path is not implemented yet).");
        }
        frag = __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_getShader).call(this, pe2.shader);
        pass = new PostEffectPass(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), frag, pe2.uniforms, (_c = pe2.persistent) != null ? _c : false, (_d = pe2.float) != null ? _d : false, void 0, false, pe2.glslVersion);
        if (pe2.persistent) {
          pass.registerBufferUniform("backbuffer");
        }
        target = void 0;
      }
      shaderSources.push(frag);
      const generators = {};
      if (pe2.uniforms) {
        for (const [key, value] of Object.entries(pe2.uniforms)) {
          if (typeof value === "function") {
            generators[key] = value;
          }
        }
      }
      __classPrivateFieldGet12(this, _VFXPlayer_postEffectEntries, "f").push({ pass, target, generators });
    }
    for (const p of passItems) {
      if (p.target) {
        __classPrivateFieldGet12(this, _VFXPlayer_postEffectBufferTargets, "f").set(p.target, void 0);
      }
    }
    const allTargetNames = __classPrivateFieldGet12(this, _VFXPlayer_postEffectEntries, "f").map((e) => e.target).filter((n) => n !== void 0);
    for (let i = 0; i < __classPrivateFieldGet12(this, _VFXPlayer_postEffectEntries, "f").length; i++) {
      for (const name of allTargetNames) {
        if (shaderSources[i].match(new RegExp(`uniform\\s+sampler2D\\s+${name}\\b`))) {
          __classPrivateFieldGet12(this, _VFXPlayer_postEffectEntries, "f")[i].pass.registerBufferUniform(name);
        }
      }
    }
  }, _VFXPlayer_initPostEffectChain = function _VFXPlayer_initPostEffectChain2(pe, rawEffect) {
    var _a;
    if (pe.shader !== void 0) {
      console.warn("[VFX-JS] Both `shader` and `effect` specified on post-effect; `effect` takes precedence.");
    }
    const effects = Array.isArray(rawEffect) ? [...rawEffect] : [rawEffect];
    __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_assertEffectsNotReused).call(this, effects);
    const captureHandle = makeEffectTexture(() => {
      const target = __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f");
      if (!target) {
        throw new Error("[VFX-JS] post-effect chain active without target");
      }
      return target.texture;
    }, () => {
      var _a2, _b;
      return (_b = (_a2 = __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f")) == null ? void 0 : _a2.width) != null ? _b : 0;
    }, () => {
      var _a2, _b;
      return (_b = (_a2 = __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f")) == null ? void 0 : _a2.height) != null ? _b : 0;
    });
    const vfxProps = {
      autoCrop: true,
      glslVersion: (_a = pe.glslVersion) != null ? _a : "300 es"
    };
    const chain = new EffectChain(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), __classPrivateFieldGet12(this, _VFXPlayer_quad, "f"), __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), effects, vfxProps, captureHandle, true, __classPrivateFieldGet12(this, _VFXPlayer_programCache, "f"));
    if (pe.uniforms) {
      for (const [k, v] of Object.entries(pe.uniforms)) {
        if (typeof v === "function") {
          __classPrivateFieldGet12(this, _VFXPlayer_postEffectChainGenerators, "f")[k] = v;
          __classPrivateFieldGet12(this, _VFXPlayer_postEffectChainStaticUniforms, "f")[k] = v();
        } else {
          __classPrivateFieldGet12(this, _VFXPlayer_postEffectChainStaticUniforms, "f")[k] = v;
        }
      }
    }
    __classPrivateFieldSet11(this, _VFXPlayer_postEffectChain, chain, "f");
    __classPrivateFieldSet11(this, _VFXPlayer_postEffectChainLastTime, Date.now() / 1e3, "f");
    chain.initAll().then(() => {
      if (__classPrivateFieldGet12(this, _VFXPlayer_postEffectChain, "f") === chain) {
        __classPrivateFieldSet11(this, _VFXPlayer_postEffectChainReady, true, "f");
      }
    }).catch((err) => {
      console.error("[VFX-JS] Post-effect init failed; post-effect disabled:", err);
      if (__classPrivateFieldGet12(this, _VFXPlayer_postEffectChain, "f") === chain) {
        __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_releaseEffects).call(this, __classPrivateFieldGet12(this, _VFXPlayer_postEffectChain, "f").effects);
        __classPrivateFieldGet12(this, _VFXPlayer_postEffectChain, "f").dispose();
        __classPrivateFieldSet11(this, _VFXPlayer_postEffectChain, null, "f");
        __classPrivateFieldSet11(this, _VFXPlayer_postEffectChainReady, false, "f");
      }
    });
  }, _VFXPlayer_runPostEffectChain = function _VFXPlayer_runPostEffectChain2(viewportGlRect, now) {
    const chain = __classPrivateFieldGet12(this, _VFXPlayer_postEffectChain, "f");
    if (!chain) {
      return;
    }
    const pr = __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
    const resolvedUniforms = __spreadValues({}, __classPrivateFieldGet12(this, _VFXPlayer_postEffectChainStaticUniforms, "f"));
    for (const [k, gen] of Object.entries(__classPrivateFieldGet12(this, _VFXPlayer_postEffectChainGenerators, "f"))) {
      resolvedUniforms[k] = gen();
    }
    const canvasW = __classPrivateFieldGet12(this, _VFXPlayer_canvasRect, "f").right - __classPrivateFieldGet12(this, _VFXPlayer_canvasRect, "f").left;
    const canvasH = __classPrivateFieldGet12(this, _VFXPlayer_canvasRect, "f").bottom - __classPrivateFieldGet12(this, _VFXPlayer_canvasRect, "f").top;
    const prev = __classPrivateFieldGet12(this, _VFXPlayer_postEffectChainLastTime, "f");
    const deltaTime = now - prev;
    __classPrivateFieldSet11(this, _VFXPlayer_postEffectChainLastTime, now, "f");
    const canvasSize = [canvasW, canvasH];
    const canvasBufferSize = [canvasW * pr, canvasH * pr];
    const canvasOnCanvas = {
      x: viewportGlRect.x * pr,
      y: viewportGlRect.y * pr,
      w: viewportGlRect.w * pr,
      h: viewportGlRect.h * pr
    };
    chain.run({
      time: now - __classPrivateFieldGet12(this, _VFXPlayer_initTime, "f"),
      deltaTime,
      mouse: [__classPrivateFieldGet12(this, _VFXPlayer_mouseX, "f") * pr, __classPrivateFieldGet12(this, _VFXPlayer_mouseY, "f") * pr],
      mouseViewport: [__classPrivateFieldGet12(this, _VFXPlayer_mouseX, "f") * pr, __classPrivateFieldGet12(this, _VFXPlayer_mouseY, "f") * pr],
      intersection: 1,
      enterTime: 0,
      leaveTime: 0,
      resolvedUniforms,
      canvasSize,
      canvasBufferSize,
      elementSize: canvasSize,
      elementBufferSize: canvasBufferSize,
      elementRectOnCanvasPx: canvasOnCanvas,
      finalTarget: null,
      isVisible: true
    });
  }, _VFXPlayer_renderPostEffects = function _VFXPlayer_renderPostEffects2(viewportGlRect, now) {
    if (!__classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f")) {
      return;
    }
    let inputTexture = __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f").texture;
    const resolvedTargets = /* @__PURE__ */ new Map();
    for (const { pass, target } of __classPrivateFieldGet12(this, _VFXPlayer_postEffectEntries, "f")) {
      if (target && pass.backbuffer) {
        resolvedTargets.set(target, pass.backbuffer.texture);
      }
    }
    for (let i = 0; i < __classPrivateFieldGet12(this, _VFXPlayer_postEffectEntries, "f").length; i++) {
      const { pass, target: targetName, generators } = __classPrivateFieldGet12(this, _VFXPlayer_postEffectEntries, "f")[i];
      const isLastPass = i === __classPrivateFieldGet12(this, _VFXPlayer_postEffectEntries, "f").length - 1;
      const mouseX = __classPrivateFieldGet12(this, _VFXPlayer_mouseX, "f") + __classPrivateFieldGet12(this, _VFXPlayer_paddingX, "f");
      const mouseY = __classPrivateFieldGet12(this, _VFXPlayer_mouseY, "f") + __classPrivateFieldGet12(this, _VFXPlayer_paddingY, "f");
      const targetDims = pass.size;
      if (targetDims) {
        const [tw, th] = targetDims;
        pass.uniforms.src.value = inputTexture;
        pass.uniforms.resolution.value.set(tw, th);
        pass.uniforms.offset.value.set(0, 0);
        pass.uniforms.time.value = now - __classPrivateFieldGet12(this, _VFXPlayer_initTime, "f");
        pass.uniforms.mouse.value.set(mouseX / viewportGlRect.w * tw, mouseY / viewportGlRect.h * th);
      } else {
        pass.setUniforms(inputTexture, __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), viewportGlRect, now - __classPrivateFieldGet12(this, _VFXPlayer_initTime, "f"), mouseX, mouseY);
      }
      pass.uniforms.passIndex.value = i;
      pass.updateCustomUniforms(generators);
      for (const [name, tex] of resolvedTargets) {
        const u = pass.uniforms[name];
        if (u) {
          u.value = tex;
        }
      }
      if (isLastPass) {
        if (pass.backbuffer) {
          if (pass.uniforms.backbuffer) {
            pass.uniforms.backbuffer.value = pass.backbuffer.texture;
          }
          __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_render).call(this, pass.pass, pass.backbuffer.target, viewportGlRect, pass.uniforms, true);
          pass.backbuffer.swap();
          __classPrivateFieldGet12(this, _VFXPlayer_copyPass, "f").setUniforms(pass.backbuffer.texture, __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), viewportGlRect);
          __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_render).call(this, __classPrivateFieldGet12(this, _VFXPlayer_copyPass, "f").pass, null, viewportGlRect, __classPrivateFieldGet12(this, _VFXPlayer_copyPass, "f").uniforms, false);
        } else {
          __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_render).call(this, pass.pass, null, viewportGlRect, pass.uniforms, false);
        }
      } else if (pass.backbuffer) {
        if (pass.uniforms.backbuffer) {
          pass.uniforms.backbuffer.value = pass.backbuffer.texture;
        }
        const bbRect = targetDims ? getGLRect(0, 0, targetDims[0] / __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), targetDims[1] / __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f")) : viewportGlRect;
        __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_render).call(this, pass.pass, pass.backbuffer.target, bbRect, pass.uniforms, true);
        pass.backbuffer.swap();
        inputTexture = pass.backbuffer.texture;
        if (targetName) {
          resolvedTargets.set(targetName, pass.backbuffer.texture);
        }
      } else {
        const bufferName = targetName != null ? targetName : `postEffect${i}`;
        let rt = __classPrivateFieldGet12(this, _VFXPlayer_postEffectBufferTargets, "f").get(bufferName);
        const rtW = targetDims ? targetDims[0] : viewportGlRect.w * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
        const rtH = targetDims ? targetDims[1] : viewportGlRect.h * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
        if (!rt || rt.width !== rtW || rt.height !== rtH) {
          rt == null ? void 0 : rt.dispose();
          rt = createRenderTarget(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), rtW, rtH, {
            float: pass.float
          });
          __classPrivateFieldGet12(this, _VFXPlayer_postEffectBufferTargets, "f").set(bufferName, rt);
        }
        const renderRect = targetDims ? getGLRect(0, 0, targetDims[0] / __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"), targetDims[1] / __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f")) : viewportGlRect;
        __classPrivateFieldGet12(this, _VFXPlayer_instances, "m", _VFXPlayer_render).call(this, pass.pass, rt, renderRect, pass.uniforms, true);
        inputTexture = rt.texture;
        if (targetName) {
          resolvedTargets.set(targetName, rt.texture);
        }
      }
    }
  }, _VFXPlayer_setupPostEffectTarget = function _VFXPlayer_setupPostEffectTarget2(width, height) {
    var _a;
    const targetWidth = width * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
    const targetHeight = height * __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f");
    if (!__classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f") || __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f").width !== targetWidth || __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f").height !== targetHeight) {
      (_a = __classPrivateFieldGet12(this, _VFXPlayer_postEffectTarget, "f")) == null ? void 0 : _a.dispose();
      __classPrivateFieldSet11(this, _VFXPlayer_postEffectTarget, createRenderTarget(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), targetWidth, targetHeight), "f");
    }
    for (const { pass } of __classPrivateFieldGet12(this, _VFXPlayer_postEffectEntries, "f")) {
      if (pass.persistent && !pass.backbuffer) {
        pass.initializeBackbuffer(__classPrivateFieldGet12(this, _VFXPlayer_ctx, "f"), width, height, __classPrivateFieldGet12(this, _VFXPlayer_pixelRatio, "f"));
      } else if (pass.backbuffer) {
        pass.resizeBackbuffer(width, height);
      }
    }
  };
  function isRectInViewport(viewport, rect) {
    return rect.left <= viewport.right && rect.right >= viewport.left && rect.top <= viewport.bottom && rect.bottom >= viewport.top;
  }
  function checkIntersection(viewport, rect, intersection, threshold) {
    if (threshold === 0) {
      return isRectInViewport(viewport, rect);
    } else {
      return intersection >= threshold;
    }
  }
  function parseOverflowOpts(overflow) {
    if (overflow === true) {
      return [true, MARGIN_ZERO];
    }
    if (overflow === void 0) {
      return [false, MARGIN_ZERO];
    }
    return [false, createMargin(overflow)];
  }
  function parseIntersectionOpts(intersectionOpts) {
    var _a, _b;
    const threshold = (_a = intersectionOpts == null ? void 0 : intersectionOpts.threshold) != null ? _a : 0;
    const rootMargin = createMargin((_b = intersectionOpts == null ? void 0 : intersectionOpts.rootMargin) != null ? _b : 0);
    return {
      threshold,
      rootMargin
    };
  }
  function readTextureSourceDim(tex, axis) {
    const src = tex.source;
    if (!src) {
      return 0;
    }
    if (typeof HTMLImageElement !== "undefined" && src instanceof HTMLImageElement) {
      return axis === "w" ? src.naturalWidth : src.naturalHeight;
    }
    if (typeof HTMLVideoElement !== "undefined" && src instanceof HTMLVideoElement) {
      return axis === "w" ? src.videoWidth : src.videoHeight;
    }
    const wc = src;
    return axis === "w" ? wc.width : wc.height;
  }
  function parseWrapSingle(wrapOpt) {
    if (wrapOpt === "repeat") {
      return "repeat";
    }
    if (wrapOpt === "mirror") {
      return "mirror";
    }
    return "clamp";
  }
  function parseWrap(wrapOpt) {
    if (!wrapOpt) {
      return ["clamp", "clamp"];
    }
    if (Array.isArray(wrapOpt)) {
      return [parseWrapSingle(wrapOpt[0]), parseWrapSingle(wrapOpt[1])];
    }
    const w = parseWrapSingle(wrapOpt);
    return [w, w];
  }
  function clamp2(x, xmin, xmax) {
    return Math.max(xmin, Math.min(xmax, x));
  }
  function isTextPathElement(element) {
    return !(element instanceof HTMLImageElement || element instanceof HTMLVideoElement || element instanceof HTMLCanvasElement);
  }

  // node_modules/@vfx-js/core/lib/esm/webgl-support.js
  function isWebGLAvailable() {
    try {
      const canvas = document.createElement("canvas");
      const gl = canvas.getContext("webgl2") || canvas.getContext("webgl");
      return gl !== null;
    } catch (e) {
      return false;
    }
  }

  // node_modules/@vfx-js/core/lib/esm/vfx.js
  var __classPrivateFieldSet12 = function(receiver, state2, value, kind, f) {
    if (kind === "m") throw new TypeError("Private method is not writable");
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
    return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state2.set(receiver, value), value;
  };
  var __classPrivateFieldGet13 = function(receiver, state2, kind, f) {
    if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
    if (typeof state2 === "function" ? receiver !== state2 || !f : !state2.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
    return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state2.get(receiver);
  };
  var _VFX_instances;
  var _VFX_player;
  var _VFX_canvas;
  var _VFX_wrapperCanvases;
  var _VFX_addImage;
  var _VFX_addVideo;
  var _VFX_addCanvas;
  var _VFX_addText;
  function checkEnvironment() {
    if (typeof window === "undefined") {
      throw "Cannot find 'window'. VFX-JS only runs on the browser.";
    }
    if (typeof document === "undefined") {
      throw "Cannot find 'document'. VFX-JS only runs on the browser.";
    }
  }
  function getCanvasStyle(fixed) {
    return {
      position: fixed ? "fixed" : "absolute",
      top: 0,
      left: 0,
      // Sized by VFXPlayer#updateCanvasSize; avoid 100vw/100vh which
      // can cause overflow on iOS Safari.
      width: "0px",
      height: "0px",
      "z-index": 9999,
      "pointer-events": "none"
    };
  }
  var VFX = class _VFX {
    /**
     * Create a VFX instance if WebGL is available, or return `null`.
     */
    static init(options) {
      try {
        return new _VFX(options);
      } catch (e) {
        return null;
      }
    }
    /**
     * Creates VFX instance and start playing immediately.
     * @throws When WebGL is not available in the current environment.
     */
    constructor(options = {}) {
      var _a;
      _VFX_instances.add(this);
      _VFX_player.set(this, void 0);
      _VFX_canvas.set(this, void 0);
      _VFX_wrapperCanvases.set(this, /* @__PURE__ */ new Map());
      checkEnvironment();
      if (!isWebGLAvailable()) {
        throw new Error("[VFX-JS] WebGL is not available in this environment.");
      }
      const opts = getVFXOpts(options);
      const canvas = document.createElement("canvas");
      const canvasStyle = getCanvasStyle(opts.fixedCanvas);
      for (const [k, v] of Object.entries(canvasStyle)) {
        canvas.style.setProperty(k, v.toString());
      }
      if (opts.zIndex !== void 0) {
        canvas.style.setProperty("z-index", opts.zIndex.toString());
      }
      ((_a = opts.wrapper) != null ? _a : document.body).appendChild(canvas);
      __classPrivateFieldSet12(this, _VFX_canvas, canvas, "f");
      __classPrivateFieldSet12(this, _VFX_player, new VFXPlayer(opts, canvas), "f");
      if (opts.autoplay) {
        __classPrivateFieldGet13(this, _VFX_player, "f").play();
      }
    }
    /**
     * Register an element to track the position and render visual effects in the area.
     */
    async add(element, opts, initialCapture) {
      if (element instanceof HTMLImageElement) {
        await __classPrivateFieldGet13(this, _VFX_instances, "m", _VFX_addImage).call(this, element, opts);
      } else if (element instanceof HTMLVideoElement) {
        await __classPrivateFieldGet13(this, _VFX_instances, "m", _VFX_addVideo).call(this, element, opts);
      } else if (element instanceof HTMLCanvasElement) {
        if (element.hasAttribute("layoutsubtree") && initialCapture) {
          await __classPrivateFieldGet13(this, _VFX_player, "f").addElement(element, opts, initialCapture);
        } else {
          await __classPrivateFieldGet13(this, _VFX_instances, "m", _VFX_addCanvas).call(this, element, opts);
        }
      } else {
        await __classPrivateFieldGet13(this, _VFX_instances, "m", _VFX_addText).call(this, element, opts);
      }
    }
    /**
     * Update the HIC texture for a layoutsubtree canvas.
     * @internal Used by VFXCanvas (@vfx-js/react).
     */
    updateHICTexture(canvas, offscreen) {
      __classPrivateFieldGet13(this, _VFX_player, "f").updateHICTexture(canvas, offscreen);
    }
    get maxTextureSize() {
      return __classPrivateFieldGet13(this, _VFX_player, "f").maxTextureSize;
    }
    /**
     * Register an element using html-in-canvas API.
     * Wraps the element in a `<canvas layoutsubtree>` and captures via drawElementImage.
     * Falls back to `add()` if html-in-canvas is not supported.
     */
    async addHTML(element, opts) {
      if (!supportsHtmlInCanvas()) {
        console.warn("html-in-canvas not supported, falling back to dom-to-canvas");
        return this.add(element, opts);
      }
      if (opts.overlay !== void 0) {
        console.warn("addHTML does not support overlay mode (layoutsubtree hides children). Ignoring overlay option.");
      }
      const _a = opts, { overlay: _ } = _a, hicOpts = __objRest(_a, ["overlay"]);
      let wrapper = __classPrivateFieldGet13(this, _VFX_wrapperCanvases, "f").get(element);
      if (wrapper) {
        __classPrivateFieldGet13(this, _VFX_player, "f").removeElement(wrapper);
      }
      const { canvas, initialCapture } = await wrapElement(element, {
        onCapture: (offscreen) => {
          __classPrivateFieldGet13(this, _VFX_player, "f").updateHICTexture(canvas, offscreen);
        },
        maxSize: __classPrivateFieldGet13(this, _VFX_player, "f").maxTextureSize
      });
      wrapper = canvas;
      __classPrivateFieldGet13(this, _VFX_wrapperCanvases, "f").set(element, wrapper);
      await __classPrivateFieldGet13(this, _VFX_player, "f").addElement(wrapper, hicOpts, initialCapture);
    }
    /**
     * Remove the element from VFX and stop rendering the shader.
     */
    remove(element) {
      const wrapper = __classPrivateFieldGet13(this, _VFX_wrapperCanvases, "f").get(element);
      if (wrapper) {
        unwrapElement(wrapper, element);
        __classPrivateFieldGet13(this, _VFX_wrapperCanvases, "f").delete(element);
        __classPrivateFieldGet13(this, _VFX_player, "f").removeElement(wrapper);
      } else {
        __classPrivateFieldGet13(this, _VFX_player, "f").removeElement(element);
      }
    }
    /**
     * Replace the effect chain on an already-registered effect-path
     * element in-place. Effects whose reference is unchanged keep their
     * init state and GPU resources; only added/removed effects run
     * `init` / `dispose`. The element's source texture is preserved.
     *
     * Useful for live UIs that reorder or toggle effects without paying
     * the cost of `vfx.remove` + `vfx.add` (which reloads the source).
     */
    updateEffects(element, effect) {
      var _a;
      const target = (_a = __classPrivateFieldGet13(this, _VFX_wrapperCanvases, "f").get(element)) != null ? _a : element;
      return __classPrivateFieldGet13(this, _VFX_player, "f").updateElementEffects(target, effect);
    }
    /**
     * Update the texture for the given element.
     *
     * For an `HTMLImageElement`, reloads its current `src` — call this
     * after changing `img.src`. Videos refresh automatically (no-op).
     * Otherwise re-snapshots the element's DOM subtree.
     *
     * Useful for elements whose contents change (input, textarea, or an
     * `<img>` whose `src` swaps).
     */
    async update(element) {
      const wrapper = __classPrivateFieldGet13(this, _VFX_wrapperCanvases, "f").get(element);
      if (wrapper) {
        wrapper.requestPaint();
        return;
      }
      if (element instanceof HTMLImageElement) {
        return __classPrivateFieldGet13(this, _VFX_player, "f").updateImageElement(element);
      } else if (element instanceof HTMLCanvasElement) {
        __classPrivateFieldGet13(this, _VFX_player, "f").updateCanvasElement(element);
        return;
      } else {
        return __classPrivateFieldGet13(this, _VFX_player, "f").updateTextElement(element);
      }
    }
    /**
     * Start rendering VFX.
     */
    play() {
      __classPrivateFieldGet13(this, _VFX_player, "f").play();
    }
    /**
     * Stop rendering VFX.
     * You can restart rendering by calling `VFX.play()` later.
     */
    stop() {
      __classPrivateFieldGet13(this, _VFX_player, "f").stop();
    }
    /**
     * Render the whole scene once, manually.
     * This is useful when you want to control the rendering timings manually by combining with `autoplay: false`.
     */
    render() {
      __classPrivateFieldGet13(this, _VFX_player, "f").render();
    }
    /**
     * Destroy VFX and stop rendering.
     */
    destroy() {
      for (const [element, wrapper] of __classPrivateFieldGet13(this, _VFX_wrapperCanvases, "f")) {
        unwrapElement(wrapper, element);
      }
      __classPrivateFieldGet13(this, _VFX_wrapperCanvases, "f").clear();
      __classPrivateFieldGet13(this, _VFX_player, "f").destroy();
      __classPrivateFieldGet13(this, _VFX_canvas, "f").remove();
    }
  };
  _VFX_player = /* @__PURE__ */ new WeakMap(), _VFX_canvas = /* @__PURE__ */ new WeakMap(), _VFX_wrapperCanvases = /* @__PURE__ */ new WeakMap(), _VFX_instances = /* @__PURE__ */ new WeakSet(), _VFX_addImage = function _VFX_addImage2(element, opts) {
    if (element.complete) {
      return __classPrivateFieldGet13(this, _VFX_player, "f").addElement(element, opts);
    } else {
      return new Promise((resolve) => {
        element.addEventListener("load", () => {
          __classPrivateFieldGet13(this, _VFX_player, "f").addElement(element, opts);
          resolve();
        }, { once: true });
      });
    }
  }, _VFX_addVideo = function _VFX_addVideo2(element, opts) {
    if (element.readyState >= 3) {
      return __classPrivateFieldGet13(this, _VFX_player, "f").addElement(element, opts);
    } else {
      return new Promise((resolve) => {
        element.addEventListener("canplay", () => {
          __classPrivateFieldGet13(this, _VFX_player, "f").addElement(element, opts);
          resolve();
        }, { once: true });
      });
    }
  }, _VFX_addCanvas = function _VFX_addCanvas2(element, opts) {
    return __classPrivateFieldGet13(this, _VFX_player, "f").addElement(element, opts);
  }, _VFX_addText = function _VFX_addText2(element, opts) {
    return __classPrivateFieldGet13(this, _VFX_player, "f").addElement(element, opts);
  };

  // src/main.js
  var SHEEN = `
precision highp float;
uniform vec2 resolution;
uniform vec2 offset;
uniform float time;
uniform sampler2D src;
out vec4 outColor;

void main() {
  vec2 uv = (gl_FragCoord.xy - offset) / resolution;
  vec4 col = texture(src, uv);
  float breath = 0.45 + 0.55 * (0.5 + 0.5 * sin(time * 2.1));
  outColor = vec4(col.rgb, col.a * breath);
}
`;
  var reducedQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  var state = {
    stack: ["zdog", "glfx", "@vfx-js/core"],
    zdog: false,
    glfx: false,
    vfx: false,
    reduced: reducedQuery.matches,
    paused: reducedQuery.matches,
    grade: "foto directa"
  };
  window.__CAPTOORA_MOTION__ = state;
  var lente = document.querySelector("#lente");
  var marco = document.querySelector("#marco");
  var retrato = document.querySelector("#retrato");
  var placa = document.querySelector("#placa");
  var pausa = document.querySelector("#pausa");
  var estado = document.querySelector("#estado");
  var lectura = document.querySelector("#lectura");
  var illo = null;
  var iris = null;
  var dragging = false;
  var gradeCanvas = null;
  var gradeTexture = null;
  var vfx = null;
  var raf = 0;
  var lastGrade = 0;
  var lastFrame = 0;
  var muestras = [];
  var ultimaVi\u00F1eta = null;
  var arranque = performance.now();
  function decir(texto) {
    if (estado) estado.textContent = texto;
  }
  function pintarLectura(vignette) {
    if (!lectura) return;
    const zdogTxt = state.zdog ? state.paused ? "quieto" : "girando" : "no arranc\xF3";
    const glfxTxt = state.glfx ? state.grade : "foto directa";
    const vfxTxt = state.vfx ? state.paused ? "en pausa" : "latido" : "HTML plano";
    const vi\u00F1eta = typeof vignette === "number" ? vignette.toFixed(2) : "\u2014";
    lectura.textContent = `Zdog: ${zdogTxt}. glfx.js: ${glfxTxt}, vi\xF1eta ${vi\u00F1eta}. VFX-JS: ${vfxTxt}.`;
  }
  function crearLente() {
    illo = new import_zdog.default.Illustration({
      element: lente,
      zoom: 1.05,
      dragRotate: true,
      resize: true,
      onDragStart() {
        dragging = true;
      },
      onDragEnd() {
        dragging = false;
      }
    });
    new import_zdog.default.Cylinder({
      addTo: illo,
      diameter: 118,
      length: 26,
      stroke: false,
      color: "#e6c56a",
      backface: "#6a5424"
    });
    new import_zdog.default.Ellipse({
      addTo: illo,
      diameter: 132,
      stroke: 7,
      color: "#f0d78c",
      translate: { z: 14 }
    });
    iris = new import_zdog.default.Group({ addTo: illo, translate: { z: 16 } });
    const pasos = 6;
    for (let i = 0; i < pasos; i += 1) {
      const ancla = new import_zdog.default.Group({
        addTo: iris,
        rotate: { z: Math.PI * 2 * i / pasos }
      });
      new import_zdog.default.RoundedRect({
        addTo: ancla,
        width: 54,
        height: 16,
        cornerRadius: 8,
        stroke: 3,
        fill: true,
        color: "#1a140c",
        translate: { x: 28 }
      });
    }
    new import_zdog.default.Ellipse({
      addTo: illo,
      diameter: 34,
      stroke: 14,
      fill: true,
      color: "#070604",
      translate: { z: 20 }
    });
    new import_zdog.default.Ellipse({
      addTo: illo,
      diameter: 8,
      stroke: 3,
      fill: true,
      color: "#fff6d8",
      translate: { x: -8, y: -8, z: 24 }
    });
    illo.rotate.x = 0.35;
    illo.rotate.y = -0.45;
    illo.updateRenderGraph();
    state.zdog = true;
  }
  function prepararGrado(img) {
    const maxAncho = 800;
    const escala = Math.min(1, maxAncho / img.naturalWidth);
    const ancho = Math.max(2, Math.round(img.naturalWidth * escala));
    const alto = Math.max(2, Math.round(img.naturalHeight * escala));
    const fuente = document.createElement("canvas");
    fuente.width = ancho;
    fuente.height = alto;
    const ctx = fuente.getContext("2d", { alpha: false });
    ctx.drawImage(img, 0, 0, ancho, alto);
    gradeCanvas = import_glfx.default.canvas();
    gradeTexture = gradeCanvas.texture(fuente);
    gradeCanvas.className = "grado";
    gradeCanvas.setAttribute(
      "aria-label",
      "El mismo retrato, con vi\xF1eta y luz movidas por glfx.js. Sigue el encuadre completo."
    );
    gradeCanvas.style.width = "100%";
    gradeCanvas.style.height = "auto";
    aplicarGrado(0.45);
    const pieDeFoto = marco.querySelector("figcaption");
    marco.insertBefore(gradeCanvas, pieDeFoto);
    retrato.classList.add("retrato-base");
    retrato.setAttribute("aria-hidden", "true");
    state.glfx = true;
    state.grade = "WebGL1, textura " + ancho + "\xD7" + alto;
  }
  function aplicarGrado(cantidad) {
    if (!gradeCanvas) return;
    const brillo = (cantidad - 0.5) * 0.1;
    try {
      gradeCanvas.draw(gradeTexture).brightnessContrast(brillo, 0.06).sepia(0.05).vignette(0.35 + cantidad * 0.28, 0.25 + cantidad * 0.55).update();
    } catch (error) {
      console.error(error);
      soltarRevelado("filtro CSS: el revelado WebGL se cay\xF3");
      decir("El revelado WebGL se cay\xF3. La foto sigue en pantalla, con un ajuste CSS.");
    }
  }
  function gradoCss() {
    retrato.classList.add("grado-css");
    state.grade = "filtro CSS, sin WebGL";
  }
  function glfxPerdido() {
    if (!gradeCanvas || !gradeCanvas._ || !gradeCanvas._.gl) return false;
    return gradeCanvas._.gl.isContextLost();
  }
  function soltarRevelado(motivo) {
    if (gradeCanvas) {
      gradeCanvas.remove();
      gradeCanvas = null;
      gradeTexture = null;
    }
    retrato.classList.remove("retrato-base");
    retrato.removeAttribute("aria-hidden");
    retrato.classList.add("grado-css");
    state.glfx = false;
    state.grade = motivo;
  }
  function soltarBarrido() {
    if (vfx) {
      try {
        vfx.destroy();
      } catch (error) {
        console.error(error);
      }
    }
    vfx = null;
    state.vfx = false;
    placa.style.opacity = "";
  }
  async function prepararBarrido() {
    if (state.vfx) return;
    const area = window.innerWidth * window.innerHeight;
    const pixelRatio = area > 2e6 ? 0.75 : 1;
    const antes = glfxPerdido();
    if (!vfx) {
      vfx = VFX.init({
        pixelRatio,
        scrollPadding: false,
        zIndex: 2,
        autoplay: false
      });
    }
    if (!vfx) {
      decir("Este navegador no abri\xF3 WebGL2. La placa se queda en HTML. El diafragma y el retrato siguen.");
      return;
    }
    try {
      await vfx.add(placa, { shader: SHEEN, overflow: 0 });
    } catch (error) {
      soltarBarrido();
      if (glfxPerdido()) soltarRevelado("filtro CSS: WebGL se solt\xF3 al montar el barrido");
      const rect = placa.getBoundingClientRect();
      decir(
        "VFX-JS no compil\xF3 el barrido (" + Math.round(rect.width) + "\xD7" + Math.round(rect.height) + ", glfx perdido antes: " + antes + "). La placa queda en HTML."
      );
      console.error(error);
      return;
    }
    if (glfxPerdido()) {
      soltarBarrido();
      soltarRevelado("filtro CSS: el barrido se llev\xF3 el contexto de la foto");
      decir("El barrido y el revelado WebGL no cupieron juntos. Quedan el diafragma y la foto con ajuste CSS.");
      return;
    }
    state.vfx = true;
    if (!state.paused) vfx.play();
  }
  function cuadro(now) {
    raf = 0;
    if (state.paused) return;
    const dt = lastFrame ? now - lastFrame : 16;
    lastFrame = now;
    if (now - arranque > 4e3 && state.vfx) {
      muestras.push(dt);
      if (muestras.length > 45) muestras.shift();
      if (muestras.length === 45) {
        let suma = 0;
        for (let i = 0; i < muestras.length; i += 1) suma += muestras[i];
        if (suma / muestras.length > 90) {
          muestras.length = 0;
          soltarBarrido();
          decir("Se apag\xF3 el barrido de VFX-JS: el cuadro se qued\xF3 por debajo de unos 11 fps. Zdog y glfx.js siguen.");
        }
      }
    }
    const t = now / 1e3;
    if (illo && iris && !dragging) {
      iris.rotate.z = t * 0.35;
      illo.rotate.y = Math.sin(t * 0.45) * 0.7;
      illo.rotate.x = 0.28 + Math.cos(t * 0.35) * 0.12;
    }
    if (illo) illo.updateRenderGraph();
    if (gradeCanvas && now - lastGrade > 40) {
      lastGrade = now;
      ultimaVi\u00F1eta = 0.5 + 0.5 * Math.sin(t * 0.9);
      aplicarGrado(ultimaVi\u00F1eta);
    }
    pintarLectura(ultimaVi\u00F1eta);
    raf = window.requestAnimationFrame(cuadro);
  }
  function arrancar() {
    if (state.paused || raf) return;
    lastFrame = 0;
    raf = window.requestAnimationFrame(cuadro);
  }
  function detener() {
    if (raf) window.cancelAnimationFrame(raf);
    raf = 0;
    if (vfx && state.vfx) vfx.stop();
  }
  function sincronizarPausa() {
    state.paused = pausa.getAttribute("aria-pressed") === "true";
    if (state.paused) {
      detener();
      pausa.textContent = "Reanudar movimiento";
      decir(
        state.reduced ? "Movimiento reducido. El diafragma queda quieto, el retrato en un solo revelado y la placa sin barrido." : "Movimiento en pausa. El diafragma queda donde est\xE1 y el retrato conserva el \xFAltimo revelado."
      );
    } else {
      if (vfx && state.vfx) vfx.play();
      pausa.textContent = "Pausar movimiento";
      decir("Movimiento activo. Puedes arrastrar el diafragma.");
      arrancar();
    }
    pintarLectura(ultimaVi\u00F1eta);
  }
  async function iniciar() {
    try {
      crearLente();
    } catch (error) {
      decir("Zdog no pudo dibujar el diafragma en este navegador.");
      console.error(error);
    }
    const listo = new Promise((resolve) => {
      if (retrato.complete && retrato.naturalWidth) resolve();
      else {
        retrato.addEventListener("load", () => resolve(), { once: true });
        retrato.addEventListener("error", () => resolve(), { once: true });
      }
    });
    await listo;
    if (retrato.naturalWidth) {
      try {
        prepararGrado(retrato);
      } catch (error) {
        gradoCss();
        decir("WebGL no estuvo disponible para el revelado. El retrato se muestra con un ajuste CSS.");
        console.error(error);
      }
    }
    if (!state.paused) {
      try {
        await prepararBarrido();
      } catch (error) {
        state.vfx = false;
        placa.style.opacity = "";
        decir("VFX-JS no pudo montar el barrido. La placa queda en HTML.");
        console.error(error);
      }
    }
    pausa.hidden = false;
    pausa.setAttribute("aria-pressed", state.paused ? "true" : "false");
    pausa.textContent = state.paused ? "Reanudar movimiento" : "Pausar movimiento";
    pausa.addEventListener("click", () => {
      const estabaEnPausa = pausa.getAttribute("aria-pressed") === "true";
      pausa.setAttribute("aria-pressed", estabaEnPausa ? "false" : "true");
      const vaAMoverse = pausa.getAttribute("aria-pressed") === "false";
      if (vaAMoverse && !state.vfx) {
        prepararBarrido().then(() => sincronizarPausa()).catch((error) => {
          state.vfx = false;
          placa.style.opacity = "";
          console.error(error);
          sincronizarPausa();
        });
        return;
      }
      sincronizarPausa();
    });
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) detener();
      else if (!state.paused) {
        if (vfx && state.vfx) vfx.play();
        arrancar();
      }
    });
    reducedQuery.addEventListener("change", () => {
      state.reduced = reducedQuery.matches;
      pausa.setAttribute("aria-pressed", state.reduced ? "true" : "false");
      sincronizarPausa();
    });
    if (state.paused) {
      if (illo) illo.updateRenderGraph();
      if (!estado.textContent) {
        decir("Movimiento reducido. Pulsa reanudar si quieres ver el diafragma, el revelado y el barrido.");
      }
    } else {
      if (state.zdog && state.glfx && state.vfx) {
        decir("Movimiento activo. Puedes arrastrar el diafragma.");
      }
      arrancar();
    }
    pintarLectura(state.glfx ? 0.5 : null);
  }
  iniciar();
})();
/*! Bundled license information:

zdog/js/boilerplate.js:
  (*!
   * Zdog v1.1.3
   * Round, flat, designer-friendly pseudo-3D engine
   * Licensed MIT
   * https://zzz.dog
   * Copyright 2020 Metafizzy
   *)
*/
