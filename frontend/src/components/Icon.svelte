<script lang="ts" context="module">
  export type IconType =
    | "AcademicCap"
    | "AdjustmentsHorizontal"
    | "AdjustmentsVertical"
    | "ArchiveBoxArrowDown"
    | "ArchiveBoxXMark"
    | "ArchiveBox"
    | "ArrowDownCircle"
    | "ArrowDownLeft"
    | "ArrowDownOnSquareStack"
    | "ArrowDownOnSquare"
    | "ArrowDownRight"
    | "ArrowDownTray"
    | "ArrowDown"
    | "ArrowLeftCircle"
    | "ArrowLeftOnRectangle"
    | "ArrowLeft"
    | "ArrowLongDown"
    | "ArrowLongLeft"
    | "ArrowLongRight"
    | "ArrowLongUp"
    | "ArrowPathRoundedSquare"
    | "ArrowPath"
    | "ArrowRightCircle"
    | "ArrowRightOnRectangle"
    | "ArrowRight"
    | "ArrowSmallDown"
    | "ArrowSmallLeft"
    | "ArrowSmallRight"
    | "ArrowSmallUp"
    | "ArrowTopRightOnSquare"
    | "ArrowTrendingDown"
    | "ArrowTrendingUp"
    | "ArrowUpCircle"
    | "ArrowUpLeft"
    | "ArrowUpOnSquareStack"
    | "ArrowUpOnSquare"
    | "ArrowUpRight"
    | "ArrowUpTray"
    | "ArrowUp"
    | "ArrowUturnDown"
    | "ArrowUturnLeft"
    | "ArrowUturnRight"
    | "ArrowUturnUp"
    | "ArrowsPointingIn"
    | "ArrowsPointingOut"
    | "ArrowsRightLeft"
    | "ArrowsUpDown"
    | "AtSymbol"
    | "Backspace"
    | "Backward"
    | "Banknotes"
    | "Bars2"
    | "Bars3BottomLeft"
    | "Bars3BottomRight"
    | "Bars3CenterLeft"
    | "Bars3"
    | "Bars4"
    | "BarsArrowDown"
    | "BarsArrowUp"
    | "Battery0"
    | "Battery100"
    | "Battery50"
    | "Beaker"
    | "BellAlert"
    | "BellSlash"
    | "BellSnooze"
    | "Bell"
    | "BoltSlash"
    | "Bolt"
    | "BookOpen"
    | "BookmarkSlash"
    | "BookmarkSquare"
    | "Bookmark"
    | "Briefcase"
    | "BugAnt"
    | "BuildingLibrary"
    | "BuildingOffice2"
    | "BuildingOffice"
    | "BuildingStorefront"
    | "Cake"
    | "Calculator"
    | "CalendarDays"
    | "Calendar"
    | "Camera"
    | "ChartBarSquare"
    | "ChartBar"
    | "ChartPie"
    | "ChatBubbleBottomCenterText"
    | "ChatBubbleBottomCenter"
    | "ChatBubbleLeftEllipsis"
    | "ChatBubbleLeftRight"
    | "ChatBubbleLeft"
    | "ChatBubbleOvalLeftEllipsis"
    | "ChatBubbleOvalLeft"
    | "CheckBadge"
    | "CheckCircle"
    | "Check"
    | "ChevronDoubleDown"
    | "ChevronDoubleLeft"
    | "ChevronDoubleRight"
    | "ChevronDoubleUp"
    | "ChevronDown"
    | "ChevronLeft"
    | "ChevronRight"
    | "ChevronUpDown"
    | "ChevronUp"
    | "CircleStack"
    | "ClipboardDocumentCheck"
    | "ClipboardDocumentList"
    | "ClipboardDocument"
    | "Clipboard"
    | "Clock"
    | "CloudArrowDown"
    | "CloudArrowUp"
    | "Cloud"
    | "CodeBracketSquare"
    | "CodeBracket"
    | "Cog6Tooth"
    | "Cog8Tooth"
    | "Cog"
    | "CommandLine"
    | "ComputerDesktop"
    | "CpuChip"
    | "CreditCard"
    | "CubeTransparent"
    | "Cube"
    | "CurrencyBangladeshi"
    | "CurrencyDollar"
    | "CurrencyEuro"
    | "CurrencyPound"
    | "CurrencyRupee"
    | "CurrencyYen"
    | "CursorArrowRays"
    | "CursorArrowRipple"
    | "DevicePhoneMobile"
    | "DeviceTablet"
    | "DocumentArrowDown"
    | "DocumentArrowUp"
    | "DocumentChartBar"
    | "DocumentCheck"
    | "DocumentDuplicate"
    | "DocumentMagnifyingGlass"
    | "DocumentMinus"
    | "DocumentPlus"
    | "DocumentText"
    | "Document"
    | "EllipsisHorizontalCircle"
    | "EllipsisHorizontal"
    | "EllipsisVertical"
    | "EnvelopeOpen"
    | "Envelope"
    | "ExclamationCircle"
    | "ExclamationTriangle"
    | "EyeDropper"
    | "EyeSlash"
    | "Eye"
    | "FaceFrown"
    | "FaceSmile"
    | "Film"
    | "FingerPrint"
    | "Fire"
    | "Flag"
    | "FolderArrowDown"
    | "FolderMinus"
    | "FolderOpen"
    | "FolderPlus"
    | "Folder"
    | "Forward"
    | "Funnel"
    | "Gif"
    | "GiftTop"
    | "Gift"
    | "GlobeAlt"
    | "GlobeAmericas"
    | "GlobeAsiaAustralia"
    | "GlobeEuropeAfrica"
    | "HandRaised"
    | "HandThumbDown"
    | "HandThumbUp"
    | "Hashtag"
    | "Heart"
    | "HomeModern"
    | "Home"
    | "Identification"
    | "InboxArrowDown"
    | "InboxStack"
    | "Inbox"
    | "InformationCircle"
    | "Key"
    | "Language"
    | "Lifebuoy"
    | "LightBulb"
    | "Link"
    | "ListBullet"
    | "LockClosed"
    | "LockOpen"
    | "MagnifyingGlassCircle"
    | "MagnifyingGlassMinus"
    | "MagnifyingGlassPlus"
    | "MagnifyingGlass"
    | "MapPin"
    | "Map"
    | "Megaphone"
    | "Microphone"
    | "MinusCircle"
    | "MinusSmall"
    | "Minus"
    | "Moon"
    | "MusicalNote"
    | "Newspaper"
    | "NoSymbol"
    | "PaintBrush"
    | "PaperAirplane"
    | "PaperClip"
    | "PauseCircle"
    | "Pause"
    | "PencilSquare"
    | "Pencil"
    | "PhoneArrowDownLeft"
    | "PhoneArrowUpRight"
    | "PhoneXMark"
    | "Phone"
    | "Photo"
    | "PlayCircle"
    | "PlayPause"
    | "Play"
    | "PlusCircle"
    | "PlusSmall"
    | "Plus"
    | "Power"
    | "PresentationChartBar"
    | "PresentationChartLine"
    | "Printer"
    | "PuzzlePiece"
    | "QrCode"
    | "QuestionMarkCircle"
    | "QueueList"
    | "Radio"
    | "ReceiptPercent"
    | "ReceiptRefund"
    | "RectangleGroup"
    | "RectangleStack"
    | "RocketLaunch"
    | "Rss"
    | "Scale"
    | "Scissors"
    | "ServerStack"
    | "Server"
    | "Share"
    | "ShieldCheck"
    | "ShieldExclamation"
    | "ShoppingBag"
    | "ShoppingCart"
    | "SignalSlash"
    | "Signal"
    | "Sparkles"
    | "SpeakerWave"
    | "SpeakerXMark"
    | "Square2Stack"
    | "Square3Stack3d"
    | "Squares2x2"
    | "SquaresPlus"
    | "Star"
    | "StopCircle"
    | "Stop"
    | "Sun"
    | "Swatch"
    | "TableCells"
    | "Tag"
    | "Ticket"
    | "Trash"
    | "Trophy"
    | "Truck"
    | "Tv"
    | "UserCircle"
    | "UserGroup"
    | "UserMinus"
    | "UserPlus"
    | "User"
    | "Users"
    | "Variable"
    | "VideoCameraSlash"
    | "VideoCamera"
    | "ViewColumns"
    | "ViewfinderCircle"
    | "Wallet"
    | "Wifi"
    | "Window"
    | "WrenchScrewdriver"
    | "Wrench"
    | "XCircle"
    | "XMark"
    | "Star";
</script>

<script lang="ts">
  export let size:
    | Number
    | "0.5"
    | "1"
    | "2"
    | "3"
    | "4"
    | "5"
    | "6"
    | "7"
    | "8"
    | "9"
    | "10" = 4;

  export let block = false;

  export let type: IconType = null;
  export let src: string = null;
  export let theme = "default";
  export let style = "";

  let loading = true;
  let icon: any;
  let svgIcon: Element;

  async function setIcon(type: string, src: string) {
    loading = true;
    let iconBase;
    if (type) {
      const icons: any = await import("../shared/icons");
      if (icons) {
        iconBase = icons[type];
        if (!iconBase) {
          console.error(`Please import ${type} into shared/icons.ts`);
        }
        icon = iconBase?.[theme] ?? iconBase?.["default"];
      } else {
        console.error("Unable to import icons");
      }
    } else if (src) {
    } else {
      console.error(`No type or src provided to icon`);
      return;
    }
    loading = false;
  }
  $: {
    setIcon(type, src);
  }

  // Color updoot
  // TODO: find a better way to color svg
  let iconColor: string;
  export function updateColor() {
    iconColor = svgIcon ? getComputedStyle(svgIcon).color : "";
  }
  $: {
    if (svgIcon) {
      updateColor();
    }
  }
</script>

{#if loading}
  <span
    {...$$props}
    {style}
    class:h-0.5={size == 0.5}
    class:w-0.5={size == 0.5}
    class:h-1={size == 1}
    class:w-1={size == 1}
    class:h-2={size == 2}
    class:w-2={size == 2}
    class:h-3={size == 3}
    class:w-3={size == 3}
    class:h-4={size == 4}
    class:w-4={size == 4}
    class:h-5={size == 5}
    class:w-5={size == 5}
    class:h-6={size == 6}
    class:w-6={size == 6}
    class:h-7={size == 7}
    class:w-7={size == 7}
    class:h-8={size == 8}
    class:w-8={size == 8}
    class:h-9={size == 9}
    class:w-9={size == 9}
    class:h-10={size == 10}
    class:w-10={size == 10}
    class:inline-block={!block}
    class:block
  >
    &nbsp;
  </span>
{:else if src}
  <span
    bind:this={svgIcon}
    {...$$props}
    style="background-color: {iconColor}; -webkit-mask: url({src}) no-repeat center; mask: url({src}) no-repeat center; {style}"
    class:h-0.5={size == 0.5}
    class:w-0.5={size == 0.5}
    class:h-1={size == 1}
    class:w-1={size == 1}
    class:h-2={size == 2}
    class:w-2={size == 2}
    class:h-3={size == 3}
    class:w-3={size == 3}
    class:h-4={size == 4}
    class:w-4={size == 4}
    class:h-5={size == 5}
    class:w-5={size == 5}
    class:h-6={size == 6}
    class:w-6={size == 6}
    class:h-7={size == 7}
    class:w-7={size == 7}
    class:h-8={size == 8}
    class:w-8={size == 8}
    class:h-9={size == 9}
    class:w-9={size == 9}
    class:h-10={size == 10}
    class:w-10={size == 10}
    class:inline-block={!block}
    class:block
  >
    &nbsp;
  </span>
{:else if icon}
  <svg
    {...icon.a}
    {...$$props}
    xmlns="http://www.w3.org/2000/svg"
    class:h-0.5={size == 0.5}
    class:w-0.5={size == 0.5}
    class:h-1={size == 1}
    class:w-1={size == 1}
    class:h-2={size == 2}
    class:w-2={size == 2}
    class:h-3={size == 3}
    class:w-3={size == 3}
    class:h-4={size == 4}
    class:w-4={size == 4}
    class:h-5={size == 5}
    class:w-5={size == 5}
    class:h-6={size == 6}
    class:w-6={size == 6}
    class:h-7={size == 7}
    class:w-7={size == 7}
    class:h-8={size == 8}
    class:w-8={size == 8}
    class:h-9={size == 9}
    class:w-9={size == 9}
    class:h-10={size == 10}
    class:w-10={size == 10}
    class:inline={!block}
    class:block
  >
    {#each icon.path ?? [] as a}
      <path {...a} />
    {/each}
    {#each icon.rect ?? [] as a}
      <rect {...a} />
    {/each}
    {#each icon.circle ?? [] as a}
      <circle {...a} />
    {/each}
    {#each icon.polygon ?? [] as a}
      <polygon {...a} />
    {/each}
    {#each icon.polyline ?? [] as a}
      <polyline {...a} />
    {/each}
    {#each icon.line ?? [] as a}
      <line {...a} />
    {/each}
  </svg>
{:else}
  X
{/if}
