-- This file is part of config-scripts
--
-- config-scripts is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- config-scripts is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.


import XMonad
import XMonad.Hooks.EwmhDesktops
import XMonad.Hooks.DynamicLog
import XMonad.Util.Run (spawnPipe)
import Data.Monoid

import System.IO
import System.Exit

import qualified XMonad.StackSet as W
import qualified Data.Map        as M


main :: IO ()
main = do
    workspacesBar <- spawnPipe "${HOME}/.config-scripts/dock/workspaces.py"
    xmonad $ ewmh defaultConfig {
        terminal           = "urxvt",
        focusFollowsMouse  = True,
        borderWidth        = 1,
        modMask            = mod4Mask,
        workspaces         = ["chromium"] ++ map show [2..9],
        normalBorderColor  = "#2f353b",
        focusedBorderColor = "#46a4ff",

        keys               = myKeys,
        mouseBindings      = myMouseBindings,

        layoutHook         = myLayout,
        manageHook         = myManageHook,
        handleEventHook    = myEventHook,
        logHook            = myLogHook workspacesBar,
        startupHook        = myStartupHook
    }


myKeys conf@(XConfig {XMonad.modMask = modm}) = M.fromList $
    [ ((modm,               xK_Return), spawn $ XMonad.terminal conf)

    , ((modm,               xK_p     ), spawn "dmenu_run")

    , ((modm .|. shiftMask, xK_c     ), kill)

    , ((modm,               xK_space ), sendMessage NextLayout)
    , ((modm .|. shiftMask, xK_space ), setLayout $ XMonad.layoutHook conf)

    , ((modm,               xK_n     ), refresh)

    , ((modm,               xK_Tab   ), windows W.focusDown)
    , ((modm,               xK_j     ), windows W.focusDown)
    , ((modm,               xK_k     ), windows W.focusUp)
    , ((modm,               xK_m     ), windows W.focusMaster)

    , ((modm .|. shiftMask, xK_Return), windows W.swapMaster)
    , ((modm .|. shiftMask, xK_j     ), windows W.swapDown)
    , ((modm .|. shiftMask, xK_k     ), windows W.swapUp)

    , ((modm,               xK_h     ), sendMessage Shrink)
    , ((modm,               xK_l     ), sendMessage Expand)

    , ((modm,               xK_t     ), withFocused $ windows . W.sink)

    , ((modm              , xK_comma ), sendMessage (IncMasterN 1))
    , ((modm              , xK_period), sendMessage (IncMasterN (-1)))

    , ((modm .|. shiftMask, xK_q     ), io (exitWith ExitSuccess))

    , ((modm              , xK_q     ), spawn "xmonad --recompile; xmonad --restart")
    ]
    ++
    [((m .|. modm, k), windows $ f i)
        | (i, k) <- zip (XMonad.workspaces conf) [xK_1 .. xK_9]
        , (f, m) <- [(W.greedyView, 0), (W.shift, shiftMask)]]
    ++
    [((m .|. modm, key), screenWorkspace sc >>= flip whenJust (windows . f))
        | (key, sc) <- zip [xK_w, xK_e, xK_r] [0..]
        , (f, m) <- [(W.view, 0), (W.shift, shiftMask)]]


myMouseBindings (XConfig {XMonad.modMask = modm}) = M.fromList $
    [ ((modm, button1), (\w -> focus w >> mouseMoveWindow w >> windows W.shiftMaster))
    , ((modm, button2), (\w -> focus w >> windows W.shiftMaster))
    , ((modm, button3), (\w -> focus w >> mouseResizeWindow w >> windows W.shiftMaster))
    ]


myLayout = tiled ||| Mirror tiled ||| Full
  where
    tiled   = Tall nmaster delta ratio
    nmaster = 1
    ratio   = 1/2
    delta   = 3/100


myManageHook = composeAll
    [ className =? "MPlayer"             --> doFloat
    , className =? "XVroot"              --> doFloat
    , className =? "FLTK"                --> doFloat
    , className =? "processing-app-Base" --> doFloat
    ]


myEventHook = mempty


myLogHook h = dynamicLogWithPP $ defaultPP
    { ppOutput          = hPutStrLn h
	, ppCurrent         = wrap ("^bg(#46a4ff) ") (" ^bg()")
	, ppVisible         = wrap ("^bg(#353535) ") (" ^bg()")
	, ppHidden          = wrap ("^fg(#dddddd) ") (" ^fg()")
	, ppHiddenNoWindows = wrap ("^fg(#2f353b) ") (" ^fg()")
    , ppUrgent          = wrap ("^bg(#ae4747) ") (" ^bg()")
	, ppWsSep           = ""
	, ppSep             = "^fg(#204a87)|^fg()"
	, ppTitle           = wrap (" ") (" ")
	, ppLayout          = wrap ("^fg(#46a4ff) ") (" ^fg()")
	}


myStartupHook = return ()
