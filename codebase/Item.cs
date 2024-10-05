public abstract class Item
{
    // 物品的大小
    public int Size { get; set; }

    // 物品的积分值
    public int Score { get; set; }

    // 物品的抓取速度
    public int Speed { get; set; }
}

public class Gold : Item
{
    // TODO: 实现金矿的特性
}

public class Stone : Item
{
    // TODO: 实现石头的特性
}

public class Diamond : Item
{
    // TODO: 实现钻石的特性
}