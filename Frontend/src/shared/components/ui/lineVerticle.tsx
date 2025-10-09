function VerticleLine() {
  return (
    <div className="w-5">
      <div className="h-full col-start-2 row-span-5 row-start-1 border-x border-x-(--pattern-fg) bg-[image:repeating-linear-gradient(315deg,_var(--pattern-fg)_0,_var(--pattern-fg)_1px,_transparent_0,_transparent_50%)] bg-[size:10px_10px] bg-fixed [--pattern-fg:var(--color-gray-950)]/15 max-lg:hidden dark:[--pattern-fg:var(--color-white)]/10" />
    </div>
  )
}
function HorizontalLine() {
  return (
    <div className="h-4 w-full">
      <div
        className="
          w-full
          border-t
          bg-[image:repeating-linear-gradient(
            90deg,
            var(--pattern-fg) 0,
            var(--pattern-fg) 1px,
            transparent 0,
            transparent 50%
          )]
          bg-[size:10px_10px]
          bg-fixed
          [--pattern-fg:var(--color-gray-950)]/15
          dark:[--pattern-fg:var(--color-white)]/10
        "
      />
    </div>
  );
}

export { VerticleLine, HorizontalLine }
