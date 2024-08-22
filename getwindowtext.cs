internal class Program
{
    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    static extern bool EnumChildWindows(IntPtr hWndParent, EnumWindowsProc lpEnumFunc, IntPtr lParam);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    static extern IntPtr SendMessage(IntPtr hWnd, uint Msg, IntPtr wParam, StringBuilder lParam);

    const uint WM_GETTEXT = 0x000D;

    static bool EnumAllChilds(IntPtr hWnd, IntPtr lParam)
    {
        StringBuilder sb = new StringBuilder(2048);

        SendMessage(hWnd, WM_GETTEXT, new IntPtr(sb.Capacity), sb);

        if (!string.IsNullOrEmpty($"{sb}"))
        {
            Console.WriteLine($"\t{hWnd:X}\t{sb}");
        }

        EnumChildWindows(hWnd, EnumAllChilds, lParam);
        return true;
    }

    static bool EnumTopLevel(IntPtr hWnd, IntPtr lParam)
    {
        StringBuilder sb = new StringBuilder(2048);

        SendMessage(hWnd, WM_GETTEXT, new IntPtr(sb.Capacity), sb);
        Console.WriteLine($"TopLevel: hWnd: {hWnd:X}\t{(string.IsNullOrEmpty($"{sb}") ? "No Caption" : $"{sb}")}");

        // Call for child windows
        EnumChildWindows(hWnd, EnumAllChilds, lParam);

        return true;
    }

    static void Main(string[] args)
    {
        // Call for TopLevel windows
        EnumWindows(EnumTopLevel, IntPtr.Zero);
        Console.ReadLine();
    }
}