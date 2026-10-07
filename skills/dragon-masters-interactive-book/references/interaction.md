# 交互与状态实现

模板的app.js是可编辑参考实现，不是不可更改的框架。每幕action描述一个主要动作。

| 类型 | 故事用途 | 成功/取消 |
|---|---|---|
| observe | 看清线索/人物 | 图中真实目标停留到时；离开/失焦取消；键盘替代 |
| drag | 递交/搬运/装配 | 拖到真实落点并松手；错误位置归位；键盘拿起/放置 |
| hold | 等待/机械启动/专注 | 连续按住有可见进度；过早松手不提交；键盘等效 |
| trace | 书写/必须经过的真实路线 | 从起点按顺序经过路径点，松手确认；不接受任意滑动 |

只有例子需要的机械动作被演示；不把这些手势强塞进所有场景。例子没有人物自由走路或通用战斗。

## 状态模型

steps[sceneId]：0=动作未完成，1=结果可观察，2=Quiz，3=Quiz完成。主线只有3才能进入下一幕；quiz:null的中间幕在观察结果后经Continue到3，不强制附题。语言、阶段、选项顺序保存在独立bookId键中；mood由阶段推导。不会保存鼠标一半的位置。新书改id，避免与示例共用存档。

临时状态不进存档：pointer capture、动画帧、Audio实例、加载epoch和AbortController。每次渲染取消旧监听/手势；异步图片只能由当前epoch提交。图片失败保持上一个安全阶段并提供Retry，不把动作提前写成成功。

## 坐标与美术

stage保持与图片相同比例，所有热点/道具坐标使用0..100百分比。输入通过getBoundingClientRect换算；改变窗口后仍对应图像，而不是旧的像素位置。若改图片比例，必须同时改stage aspect-ratio并重新测量；模板按16:9图片设计。

道具唯一性检查包括底图，不仅DOM。装配后的齿轮作为decorative prop出现在后续幕，不能突然回到工作台。按住运转时可旋转独立齿轮层，释放/切换即取消；减小动态时只显示进度和稳定结果。

## Quiz与阅读

动作完成后先看result，自主进入Story check，避免图片闪一下就被题目盖住。Quiz阶段不渲染caption；Read story与Journal在Quiz期间隐藏并关闭；Review evidence明确退回结果/复习阶段，再进入题目。答错提示寻找证据，三次后可回看；不自动把错答算对。通过后给下一幕/合书，不增加无意义确认关卡。

## 动画升级路径

固定轨迹拖物体可用独立的`track-flight.js`，不把它误当成“只描线”。先解码背景和sprite，再挂载；path为SVG路径（0..1000场景坐标），width为画面宽度百分比。确认路径包含整个物体并避开人物/文字。动态局部搜索、连续线段投影与每帧transform更新避免快速拖动卡住，仍防止直接跳到环的终点。中途松手可接续，终点松手调用onComplete；失焦/Esc取消本次手势，destroy或AbortSignal清理全部监听与动画帧。此组件不自动更改故事存档。

```html
<script src="track-flight.js"></script>
```
```js
const flight = mountTrackFlight({
  container: document.getElementById('layers'),
  sprite: 'art/your-independent-sprite.webp',
  path: 'M200 500 C400 150 600 850 800 500',
  width: 18,
  label: 'Follow the wind',
  signal: sceneAbortController.signal,
  onComplete: () => commitThisSceneAction()
});
```

函数中的sceneAbortController和commitThisSceneAction由宿主提供；在模板app.js中可分别用当前abort和commit。0.3.0已接入action.type=track，宿主负责预解码sprite、完成保存、取消与销毁。也支持advance及quiz:null；字段见data-contract.md。

要做更复杂人物动作：先准备相同角色的分层/关键帧和干净背景，再实现固定故事动作，测试边缘、遮挡与地面接触。不要拿静态整图裁块移动假装自然动画。图片加载与声音是可失败依赖，不能绑死故事状态机。

## 整书补充

封面/说明/结尾由书籍数据读取；新建生产工程不把原创演示当成书稿。每幕chapterId、eventIds映射到制作记录。evidence在动作完成后进入Journal；retell为通过后的可选关键词排序，结果不影响主线。动作与检查点分离，允许Quiz之后仍有章末剧情。
