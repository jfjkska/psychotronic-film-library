# Liquid filters for the small WebP copies made by tools/make_thumbs.py.
#
#   {{ poster | thumb: 400 }}         → /assets/img/thumbs/posters/x-400.webp, or the
#                                        original path when that file doesn't exist
#   {{ poster | thumb_srcset: "400,600" }} → "…-400.webp 400w, …-600.webp 600w", or ""
#
# A thumbnail is used only if it exists in the source tree, so a new review
# shows its full poster until the poster workflow has made its thumbnails.
module PsychotronicThumbs
  def thumb(path, width)
    found = thumb_path(path, width)
    found || path
  end

  def thumb_srcset(path, widths)
    widths.to_s.split(",").map(&:strip).filter_map do |w|
      found = thumb_path(path, w)
      "#{@context.registers[:site].baseurl}#{found} #{w}w" if found
    end.join(", ")
  end

  private

  def thumb_path(path, width)
    return nil if path.nil? || path.to_s.empty?
    path = path.to_s
    folder = path.start_with?("/assets/img/posters/") ? "posters/" : (path == "/assets/img/banner.jpg" ? "" : nil)
    return nil if folder.nil?
    stem = File.basename(path, File.extname(path))
    candidate = "/assets/img/thumbs/#{folder}#{stem}-#{width}.webp"
    site = @context.registers[:site]
    File.exist?(File.join(site.source, candidate)) ? candidate : nil
  end
end

Liquid::Template.register_filter(PsychotronicThumbs)
